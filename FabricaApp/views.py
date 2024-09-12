from .models import (
    FormularioProyectoFabrica,
    FabricaImage,
)
from .forms import (
    ProyectoFabricaCreateForm,
    ProyectoFabricaFondosCreateForm,
    ImageFabricaForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    View,
)
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q
from django.core.paginator import Paginator
from core.mixins import PermitsPositionMixin
from django.http import HttpResponse
from django.core.mail import send_mail

# Create your views here.

######################################
### ### PROYECTO FABRICA ### ###
######################################


class ProyectoFabricaCreateView(LoginRequiredMixin, View):
    template_name = "pages/ficha/fabrica_fondos.html"

    def get(self, request, *args, **kwargs):
        parte1_form = ProyectoFabricaCreateForm()
        parte2_form = ProyectoFabricaFondosCreateForm()
        image_form = ImageFabricaForm()
        return self.render_response(request, parte1_form, image_form, parte2_form)

    def post(self, request, *args, **kwargs):
        parte1_form = ProyectoFabricaCreateForm(request.POST, request.FILES)
        image_form = ImageFabricaForm(request.POST, request.FILES)

        if parte1_form.is_valid() and image_form.is_valid():
            if parte1_form.cleaned_data["fondos"]:
                return self.handle_fondos_checked(request, parte1_form, image_form)
            else:
                return self.handle_fondos_not_checked(request, parte1_form, image_form)
        else:
            parte2_form = ProyectoFabricaFondosCreateForm()
            self.handle_form_errors(parte1_form, image_form, parte2_form)
            return self.render_response(request, parte1_form, image_form, parte2_form)

    def handle_fondos_checked(self, request, parte1_form, image_form):
        parte2_form = ProyectoFabricaFondosCreateForm(request.POST)
        if parte2_form.is_valid():
            instance = self.save_parte1_form(request, parte1_form)
            self.save_images(instance, request.FILES.getlist("image"))
            self.save_parte2_form(parte2_form, instance)
            messages.success(self.request, "Creado con éxito")
            self.send_email_notification(request.user)
            return redirect("FabriFichaCreate")
        else:
            self.handle_form_errors(parte1_form, image_form, parte2_form)
            return self.render_response(request, parte1_form, image_form, parte2_form)

    def handle_fondos_not_checked(self, request, parte1_form, image_form):
        instance = self.save_parte1_form(request, parte1_form)
        self.save_images(instance, request.FILES.getlist("image"))
        messages.success(self.request, "Creado con éxito")
        self.send_email_notification(request.user)
        return redirect("FabriFichaCreate")

    def save_parte1_form(self, request, form):
        instance = form.save(commit=False)
        instance.user_id = request.user
        instance.save()
        return instance

    def save_images(self, instance, images):
        for image in images:
            FabricaImage.objects.create(ficha_fabrica=instance, image=image)

    def save_parte2_form(self, form, instance):
        fondos_instance = form.save(commit=False)
        fondos_instance.proyecto = instance
        fondos_instance.save()

    def send_email_notification(self, user):
        subject = f"Mensaje de {user}"
        message_body = (
            f"Mensaje enviado por {user} ({user.email}):\n\nRegistro de nuevo proyecto"
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ["destinatario@dominio.com"]
        send_mail(subject, message_body, from_email, recipient_list)

    def handle_form_errors(self, proyecto_form, img_form, fondos_form):
        combined_errors = {}

        errors = [proyecto_form, img_form]
        if proyecto_form.cleaned_data.get("fondos", False):
            errors.append(fondos_form)

        # Combinar errores de todos los formularios
        for form in errors:
            for field, field_errors in form.errors.items():
                combined_errors.setdefault(field, []).extend(field_errors)

        # Registrar los mensajes de error
        for field, field_errors in combined_errors.items():
            for error in field_errors:
                messages.error(self.request, error)

    def render_response(self, request, parte1_form, image_form, parte2_form):
        return render(
            request,
            self.template_name,
            {
                "parte1_form": parte1_form,
                "image_form": image_form,
                "parte2_form": parte2_form,
            },
        )


class ProyectoFabricaListView(LoginRequiredMixin, ListView):
    model = FormularioProyectoFabrica
    template_name = "pages/ficha/fabrica_lista.html"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-id")
        user = self.request.user
        search_query = self.request.GET.get("search")

        # Filtrar según el usuario
        if not user.is_superuser:
            queryset = queryset.filter(user_id=user.id)

        # Filtrar por código SIR si se ha proporcionado una búsqueda
        if search_query:
            queryset = queryset.filter(
                Q(codigo_sir=search_query) | Q(nombre_propuesta__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context["object_list"], self.paginate_by)
        page = self.request.GET.get("page")
        context["object_list"] = paginator.get_page(page)
        context["placeholder"] = "Buscar por código SIR o Nombre de la propuesta."
        return context


class ProyectoFabricaDetailView(LoginRequiredMixin, DetailView):
    model = FormularioProyectoFabrica
    template_name = "pages/ficha/fabrica_detalle.html"
    context_object_name = "item"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(self.model, id=id_)


class ProyectoFabricaUpdateView(LoginRequiredMixin, View):
    template_name = "pages/ficha/fabrica_update.html"

    def get(self, request, *args, **kwargs):
        id_ = self.kwargs.get("pk")
        proyecto = get_object_or_404(FormularioProyectoFabrica, id=id_)

        proyecto_form = ProyectoFabricaCreateForm(instance=proyecto)

        fondos_form = ProyectoFabricaFondosCreateForm(
            instance=(
                proyecto.fondos_proyecto.first()
                if proyecto.fondos_proyecto.exists()
                else None
            )
        )
        return self.render_response(request, proyecto, proyecto_form, fondos_form)

    def post(self, request, *args, **kwargs):
        id_ = self.kwargs.get("pk")
        proyecto = get_object_or_404(FormularioProyectoFabrica, id=id_)

        proyecto_form = ProyectoFabricaCreateForm(
            request.POST, request.FILES, instance=proyecto
        )

        fondos_form = ProyectoFabricaFondosCreateForm(
            request.POST,
            instance=proyecto.fondos_proyecto.first() if proyecto.fondos else None,
        )

        if proyecto_form.is_valid():
            return self.handle_valid_project_form(request, proyecto_form, fondos_form)
        else:
            self.handle_form_errors(proyecto_form, fondos_form)
            return self.render_response(request, proyecto, proyecto_form, fondos_form)

    def get_formatted_start_date(self, proyecto):
        return (
            proyecto.fecha_inicio.strftime("%Y-%m-%d") if proyecto.fecha_inicio else ""
        )

    def handle_valid_project_form(self, request, proyecto_form, fondos_form):
        proyecto = proyecto_form.save(commit=False)
        if proyecto_form.cleaned_data.get("fondos"):
            if fondos_form.is_valid():
                self.save_fondos_form(fondos_form, proyecto)
            else:
                self.handle_form_errors(proyecto_form, fondos_form)
                return self.render_response(
                    request, proyecto, proyecto_form, fondos_form
                )

        proyecto.save()
        messages.success(request, "Proyecto actualizado exitosamente.")
        return redirect("FabriFichaList")

    def save_fondos_form(self, fondos_form, proyecto):
        fondos = fondos_form.save(commit=False)
        fondos.proyecto = proyecto
        fondos.save()

    def handle_form_errors(self, proyecto_form, fondos_form):
        combined_errors = {}

        errors = [proyecto_form]
        if proyecto_form.cleaned_data.get("fondos", False):
            errors.append(fondos_form)

        # Combinar errores de todos los formularios
        for form in errors:
            for field, field_errors in form.errors.items():
                combined_errors.setdefault(field, []).extend(field_errors)

        # Registrar los mensajes de error
        for field, field_errors in combined_errors.items():
            for error in field_errors:
                messages.error(self.request, error)

    def render_response(self, request, proyecto, proyecto_form, fondos_form):
        return render(
            request,
            self.template_name,
            {
                "proyecto_form": proyecto_form,
                "fondos_form": fondos_form,
                "fecha_inicio": request.POST.get(
                    "fecha_inicio", self.get_formatted_start_date(proyecto)
                ),
            },
        )


class ProyectoFabricaDeleteView(LoginRequiredMixin, PermitsPositionMixin, DeleteView):
    model = FormularioProyectoFabrica
    success_url = reverse_lazy("FabriFichaList")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "Proyecto eliminado correctamente")
        self.object.delete()
        return redirect(self.get_success_url())


############################
### ###  Generate PDF
############################
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import red, HexColor
from reportlab.graphics.shapes import Drawing, Line
import os
import locale


class PdfView(View):

    def setup_pdf_response(self):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="reporte.pdf"'
        return response

    def setup_document(self, response):
        doc = SimpleDocTemplate(
            response,
            pagesize=letter,
            leftMargin=20,
            rightMargin=20,
            topMargin=30,
            bottomMargin=20,
        )
        story = []
        return doc, story

    def add_cover_images(self, story):
        static_path = settings.STATICFILES_DIRS[0]
        img_inacap = self.get_image(static_path, "img/inacap2.png", 1.5, 0.4)
        img_logo_fabrica = self.get_image(static_path, "img/logo_fabrica.png", 2, 0.5)

        table_data = self.create_image_row(img_inacap, img_logo_fabrica)
        if table_data:
            table = self.create_centered_table(
                table_data, [2 * inch, 3 * inch, 2 * inch]
            )
            story.append(table)

    def get_image(self, static_path, img_path, width, height):
        img_full_path = os.path.join(static_path, img_path)
        return (
            Image(img_full_path, width * inch, height * inch)
            if os.path.exists(img_full_path)
            else None
        )

    def create_image_row(self, img_inacap, img_logo_fabrica):
        if img_inacap or img_logo_fabrica:
            return [[img_inacap, Spacer(4 * inch, 1 * inch), img_logo_fabrica]]
        return None

    def create_centered_table(self, table_data, col_widths):
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        return table

    def add_cover_page(self, title_style, bold_style, story, formulario_proyecto):
        story.append(Spacer(1, 250))
        story.append(
            Paragraph(
                f"Reporte de Proyecto: {formulario_proyecto.nombre_propuesta}",
                title_style,
            )
        )
        story.append(Spacer(1, 280))

        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        fecha_formateada = formulario_proyecto.fecha_inicio.strftime("%d %B %Y")
        story.append(
            Paragraph(
                f"<strong>Fecha de Inicio:</strong> {fecha_formateada}", bold_style
            )
        )
        story.append(Spacer(1, 6))
        story.append(
            Paragraph(
                f"<strong>Empresa:</strong> {formulario_proyecto.empresa}", bold_style
            )
        )
        story.append(Spacer(1, 12))

        story.append(PageBreak())

    def create_red_line(self):
        drawing = Drawing()
        line_width = 550
        line = Line(0, 0, line_width, 0)
        line.strokeColor = red
        line.strokeWidth = 1
        drawing.add(line)
        drawing.height = 10
        drawing.width = line_width
        return drawing

    def add_project_paragraph(self, story, label, value, style):
        dark_gray_color = HexColor("#333333")
        story.append(
            Paragraph(
                f"<strong>{label}:</strong> <font color='{dark_gray_color}'>{value}</font>",
                style,
            )
        )
        story.append(Spacer(1, 12))

    def add_project_details(
        self, red_bold_style, normal_style, story, formulario_proyecto
    ):

        story.append(
            Paragraph("<strong>Detalles del Proyecto</strong>", red_bold_style)
        )
        story.append(self.create_red_line())
        story.append(Spacer(1, 24))

        self.add_project_paragraph(
            story, "Empresa", formulario_proyecto.empresa, normal_style
        )
        self.add_project_paragraph(
            story,
            "Docente líder",
            f"{formulario_proyecto.docente_id.nombre} {formulario_proyecto.docente_id.apellido_p}",
            normal_style,
        )
        self.add_project_paragraph(
            story, "Problema/Desafío", formulario_proyecto.problema, normal_style
        )
        self.add_project_paragraph(
            story, "Objetivo", formulario_proyecto.objetivo, normal_style
        )

        story.append(PageBreak())

    def add_project_images(
        self, normal_style, red_bold_style, story, formulario_proyecto
    ):

        story.append(
            Paragraph("<strong>Imágenes del Proyecto</strong>", red_bold_style)
        )
        story.append(self.create_red_line())
        story.append(Spacer(1, 24))

        images = [
            Image(image.image.path, 3 * inch, 3 * inch)
            for image in formulario_proyecto.images.all()
        ]  # Tamaño aumentado

        # Crear tabla para las imágenes en dos columnas
        if images:
            image_table_data = []
            for i in range(0, len(images), 2):
                row = images[i : i + 2]
                image_table_data.append(row)

            image_table = Table(
                image_table_data, colWidths=[3.5 * inch] * 2
            )  # Ajustar el ancho de las columnas
            image_table.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("SPACEBEFORE", (0, 0), (-1, 0), 12),
                        ("SPACEAFTER", (0, 0), (-1, -1), 12),
                    ]
                )
            )
            story.append(image_table)
        else:
            story.append(Paragraph("No hay imágenes disponibles.", normal_style))

        story.append(PageBreak())

    def add_funds_info(self, red_bold_style, normal_style, story, formulario_proyecto):
        if formulario_proyecto.fondos:

            story.append(
                Paragraph("<strong>Postulación a Fondos</strong>", red_bold_style)
            )
            story.append(self.create_red_line())
            story.append(Spacer(1, 24))

            fondos = formulario_proyecto.fondos_proyecto.first()
            self.add_funds_paragraph(
                story,
                "Technology Readiness Levels (TRL)",
                fondos.trl_id.id,
                normal_style,
            )
            self.add_funds_paragraph(
                story, "Problema/Oportunidad", fondos.problema_oportunidad, normal_style
            )
            self.add_funds_paragraph(
                story, "Solución Innovadora", fondos.solucion_innovadora, normal_style
            )
            self.add_funds_paragraph(
                story, "Plan de Trabajo", fondos.plan_trabajo, normal_style
            )
            self.add_funds_paragraph(
                story,
                "Potencial de Comercialización",
                fondos.potencial_comercializacion,
                normal_style,
            )

    def add_funds_paragraph(self, story, label, value, style):
        dark_gray_color = HexColor("#333333")
        story.append(
            Paragraph(
                f"<strong>{label}:</strong> <font color='{dark_gray_color}'>{value}</font>",
                style,
            )
        )
        story.append(Spacer(1, 12))

    def generate_pdf(self, formulario_proyecto):
        response = self.setup_pdf_response()
        doc, story = self.setup_document(response)

        # Estilos
        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]
        title_style = styles["Title"]
        bold_style = ParagraphStyle(
            name="Bold", parent=styles["Normal"], fontName="Helvetica-Bold"
        )
        red_bold_style = ParagraphStyle(
            name="RedBold",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=red,
        )
        dark_gray_color = HexColor("#333333")

        # Crear estilos personalizados para los párrafos

        normal_style.fontSize = 12
        normal_style.leading = 20
        normal_style.textColor = dark_gray_color
        normal_style.spaceAfter = 12

        #############################################
        # Imágenes de portada desde static

        self.add_cover_images(story)

        #############################################
        # Portada
        self.add_cover_page(title_style, bold_style, story, formulario_proyecto)

        ##############################################
        # Nueva página para el contenido
        self.add_project_details(
            red_bold_style, normal_style, story, formulario_proyecto
        )

        ##############################################
        # Nueva página para el contenido

        self.add_project_images(
            normal_style, red_bold_style, story, formulario_proyecto
        )

        ##############################################
        # Nueva página para el contenido

        self.add_funds_info(red_bold_style, normal_style, story, formulario_proyecto)

        doc.build(story)
        return response

    def get(self, request, *args, **kwargs):
        cod_id = kwargs.get("pk")
        formulario_proyecto = get_object_or_404(FormularioProyectoFabrica, id=cod_id)
        return self.generate_pdf(formulario_proyecto)
