from .models import (
    FormularioProyectoInterno,
    FormularioProyectoFabrica,
    FormularioProyectoFabLab,
    FabLabImage,
)
from .forms import (
    ProyectoInternoCreateForm,
    ProyectoFabricaCreateForm,
    ProyectoFabLabCreateForm,
    ImageForm,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    View,
)
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q
from django.core.paginator import Paginator
from core.mixins import PermitsPositionMixin
from django.http import HttpResponse

# Create your views here.


####################################################
### ### PROYECTO INTERNO ###
####################################################


class ProyectoInternoCreateView(LoginRequiredMixin, CreateView):
    model = FormularioProyectoInterno
    form_class = ProyectoInternoCreateForm
    template_name = "pages/fabrica/fabrica.html"
    success_url = reverse_lazy("FabriCreate")

    def form_valid(self, form):
        user = self.request.user
        formulario_proyecto = form.save(commit=False)
        formulario_proyecto.user_id = user
        formulario_proyecto.save()
        messages.success(self.request, "Archivo cargado con éxito")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(field, error)
                messages.error(self.request, f"{error}")
        return redirect("FabriCreate")


class ProyectoInternoListView(LoginRequiredMixin, ListView):
    model = FormularioProyectoInterno
    template_name = "pages/fabrica/fabrica_lista.html"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-id")
        search_query = self.request.GET.get("search")

        if search_query:
            queryset = queryset.filter(
                Q(docente_id__run=search_query)
                | Q(docente_id__nombre__icontains=search_query)
                | Q(docente_id__apellido_p__icontains=search_query)
                | Q(docente_id__email__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context["object_list"], self.paginate_by)
        page = self.request.GET.get("page")
        context["object_list"] = paginator.get_page(page)
        context["placeholder"] = "Buscar por run, nombre, apellido o correo."
        return context


class ProyectoInternoDetailView(LoginRequiredMixin, DetailView):
    model = FormularioProyectoInterno
    template_name = "pages/fabrica/fabrica_detalle.html"
    context_object_name = "item"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(FormularioProyectoInterno, id=id_)


class ProyectoInternoDeleteView(LoginRequiredMixin, PermitsPositionMixin, DeleteView):
    model = FormularioProyectoInterno
    success_url = reverse_lazy("FabriList")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "Proyecto eliminado correctamente")
        self.object.delete()
        return redirect(self.get_success_url())


class ProyectoInternoUpdateView(LoginRequiredMixin, PermitsPositionMixin, UpdateView):
    model = FormularioProyectoInterno
    form_class = ProyectoInternoCreateForm
    template_name = "pages/fabrica/fabrica.html"
    success_url = reverse_lazy("FabriList")

    def form_valid(self, form):
        form.clean()
        form.save()
        messages.success(self.request, "Proyecto editado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return redirect("FabriList")


####################################################
### ### PROYECTO FABRICA ###
####################################################


class ProyectoFabricaCreateView(LoginRequiredMixin, CreateView):
    model = FormularioProyectoFabrica
    form_class = ProyectoFabricaCreateForm
    template_name = "pages/fabrica/fabrica.html"
    success_url = reverse_lazy("FabriFichaCreate")

    def form_valid(self, form):
        user = self.request.user
        formulario_proyecto = form.save(commit=False)
        formulario_proyecto.user_id = user
        formulario_proyecto.save()
        messages.success(self.request, "Archivo cargado con éxito")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(field, error)
                messages.error(self.request, f"{error}")
        return redirect("FabriFichaCreate")


class ProyectoFabricaListView(LoginRequiredMixin, ListView):
    model = FormularioProyectoFabrica
    template_name = "pages/ficha/fabrica_lista.html"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-id")
        search_query = self.request.GET.get("search")

        if search_query:
            queryset = queryset.filter(Q(empresa_id__nombre_empresa=search_query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context["object_list"], self.paginate_by)
        page = self.request.GET.get("page")
        context["object_list"] = paginator.get_page(page)
        context["placeholder"] = "Buscar por nombre de empresa."
        return context


class ProyectoFabricaDetailView(LoginRequiredMixin, DetailView):
    model = FormularioProyectoFabrica
    template_name = "pages/ficha/fabrica_detalle.html"
    context_object_name = "item"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(self.model, id=id_)


class ProyectoFabricaDeleteView(LoginRequiredMixin, PermitsPositionMixin, DeleteView):
    model = FormularioProyectoFabrica
    success_url = reverse_lazy("FabriFichaList")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "Proyecto eliminado correctamente")
        self.object.delete()
        return redirect(self.get_success_url())


class ProyectoFabricaUpdateView(LoginRequiredMixin, PermitsPositionMixin, UpdateView):
    model = FormularioProyectoFabrica
    form_class = ProyectoFabricaCreateForm
    template_name = "pages/fabrica/fabrica.html"
    success_url = reverse_lazy("FabriFichaList")

    def form_valid(self, form):
        form.clean()
        form.save()
        messages.success(self.request, "Proyecto editado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return redirect("FabriFichaList")


####################################################
### ### PROYECTO FABLAB ###
####################################################


class ProyectoFabLabCreateView(View):
    def get(self, request):
        fablab_form = ProyectoFabLabCreateForm()
        image_form = ImageForm()
        return render(
            request,
            "pages/fablab/fablab.html",
            {"fablab_form": fablab_form, "image_form": image_form},
        )

    def post(self, request):
        fablab_form = ProyectoFabLabCreateForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)

        if fablab_form.is_valid() and image_form.is_valid():
            user = self.request.user
            fablab = fablab_form.save(commit=False)
            fablab.user_id = user
            fablab.save()

            uploaded_images = request.FILES.getlist("image")
            for image in uploaded_images:
                FabLabImage.objects.create(ficha_fablab=fablab, image=image)

            return redirect("FabLabFichaList")

        return render(
            request,
            "pages/fablab/fablab.html",
            {"fablab_form": fablab_form, "image_form": image_form},
        )


class ProyectoFabLabListView(LoginRequiredMixin, ListView):
    model = FormularioProyectoFabLab
    template_name = "pages/fablab/fablab_lista.html"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-id")
        search_query = self.request.GET.get("search")

        if search_query:
            queryset = queryset.filter(Q(nombre_propuesta=search_query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context["object_list"], self.paginate_by)
        page = self.request.GET.get("page")
        context["object_list"] = paginator.get_page(page)
        context["placeholder"] = "Buscar por nombre de propuesta."
        return context


class ProyectoFabLabDetailView(LoginRequiredMixin, DetailView):
    model = FormularioProyectoFabLab
    template_name = "pages/fablab/fablab_detalle.html"
    context_object_name = "item"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(self.model, id=id_)


class ProyectoFabLabDeleteView(LoginRequiredMixin, PermitsPositionMixin, DeleteView):
    model = FormularioProyectoFabLab
    success_url = reverse_lazy("FabLabFichaList")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "Proyecto eliminado correctamente")
        self.object.delete()
        return redirect(self.get_success_url())


class ProyectoFabLAbUpdateView(LoginRequiredMixin, PermitsPositionMixin, UpdateView):
    model = FormularioProyectoFabLab
    form_class = ProyectoFabLabCreateForm
    template_name = "pages/fabrica/fabrica.html"
    success_url = reverse_lazy("FabLabFichaList")

    def form_valid(self, form):
        form.clean()
        form.save()
        messages.success(self.request, "Proyecto editado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error en el formulario")
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{error}")
        return redirect("FabLabFichaList")


############################
### ###  Generate PDF
############################

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab import platypus


class GeneratePdfFabricaView(LoginRequiredMixin, View):
    def generate_pdf(self, formulario_proyecto):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="reporte.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()
        # Definir un estilo para los títulos en negrita
        ParagraphStyle(name="Bold", parent=styles["Normal"], fontName="Helvetica-Bold")

        story = []

        # Título
        title = f"Título: {formulario_proyecto.nombre_propuesta}"
        story.append(Paragraph(title, styles["Title"]))
        story.append(Spacer(1, 12))

        # Imagen
        if formulario_proyecto.img:
            img_path = formulario_proyecto.img.path
            try:
                img = platypus.Image(img_path, 2 * inch, 2 * inch)
                story.append(img)
                story.append(Spacer(1, 12))
            except Exception as e:
                print(e)
                story.append(Paragraph("Error al cargar la imagen.", styles["Normal"]))

        # Detalles del proyecto
        empresa = f"<b>Empresa:</b> {formulario_proyecto.empresa_id.nombre_empresa}"
        problema = f"<b>Problema/Desafío:</b><br/>{formulario_proyecto.problema}"
        objetivos = f"<b>Objetivo:</b><br/>{formulario_proyecto.objetivos}"
        solucion = f"<b>Solución generada:</b><br/>{formulario_proyecto.solucion}"

        details = f"""
        {empresa}<br/>
        <br/>
        {problema}<br/>
        <br/>
        {objetivos}<br/>
        <br/>
        {solucion}<br/>
        """
        story.append(Paragraph(details, styles["Normal"]))
        story.append(Spacer(1, 12))

        # Equipo de proyecto
        docentes = "<br/>".join(
            [docente.nombre for docente in formulario_proyecto.docentes.all()]
        )
        equipo = f"<b>Equipo de proyecto:</b><br/>{docentes}<br/>"
        equipo += f"Alumnos IP: {formulario_proyecto.alumnos_ip}<br/>"
        equipo += f"Alumnos CFT: {formulario_proyecto.alumnos_cft}<br/>"
        story.append(Paragraph(equipo, styles["Normal"]))
        story.append(Spacer(1, 12))

        # TRL
        trl = (
            f"<b>Technology Readiness Levels (TRL):</b> {formulario_proyecto.trl_id.id}"
        )
        story.append(Paragraph(trl, styles["Normal"]))

        # Build the PDF
        doc.build(story)
        return response

    def get(self, request, *args, **kwargs):
        cod_id = kwargs.get("pk")
        formulario_proyecto = get_object_or_404(FormularioProyectoFabrica, id=cod_id)
        return self.generate_pdf(formulario_proyecto)


###########################
### ## Generate PTT ###
###########################

from io import BytesIO
from pptx import Presentation
from PIL import Image
from pptx.util import Inches, Pt


class GeneratePptFabLabView(LoginRequiredMixin, View):
    def generate_ppt(self, formulario_proyecto):
        # Crear una presentación en memoria
        presentation = Presentation()

        # Agregar una diapositiva con un título y un subtítulo
        slide_layout = presentation.slide_layouts[0]  # Título y subtítulo
        slide = presentation.slides.add_slide(slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        title.text = "FABLAB INACAP"
        subtitle.text = "Fichas de Proyecto"

        # Agregar una diapositiva con imágenes del proyecto
        if formulario_proyecto.images.exists():
            slide_layout = presentation.slide_layouts[5]  # Diapositiva en blanco
            slide = presentation.slides.add_slide(slide_layout)
            title_shape = slide.shapes.title
            title_shape.text = "Detalle del Proyecto"

            # Configurar el tamaño y la posición de las imágenes
            left_margin = Inches(0.5)
            top_margin = Inches(1.3)
            image_width = Inches(2.5)
            image_height = Inches(2.5)
            space_between_images = Inches(0.2)  # Espacio entre imágenes
            max_images_per_row = 2

            # Añadir título y TRL al lado derecho de las imágenes
            right_text_box = slide.shapes.add_textbox(
                Inches(6), Inches(1.2), Inches(4), Inches(3)
            )
            text_frame = right_text_box.text_frame
            p = text_frame.add_paragraph()
            p.text = f"Nombre propuesta:\n{formulario_proyecto.nombre_propuesta}"
            p.font.size = Pt(14)
            p.font.bold = True
            p.space_after = Pt(14)

            p = text_frame.add_paragraph()
            p.text = f"TRL:{formulario_proyecto.trl_id}"
            p.font.size = Pt(14)
            p.font.bold = True
            p.space_after = Pt(14)

            # Añadir imágenes
            row = 0
            col = 0
            for image in formulario_proyecto.images.all():
                img_stream = BytesIO(image.image.read())

                # Convertir WEBP a PNG
                with Image.open(img_stream) as img:
                    img = img.convert("RGB")  # Convertir a RGB si es necesario
                    png_io = BytesIO()
                    img.save(png_io, format="PNG")
                    png_io.seek(0)

                    # Calcular posición de la imagen
                    left = left_margin + col * (image_width + space_between_images)
                    top = top_margin + row * (image_height + space_between_images)

                    # Agregar imagen al PPT
                    slide.shapes.add_picture(
                        png_io, left, top, width=image_width, height=image_height
                    )

                    # Ajustar fila y columna para la siguiente imagen
                    col += 1
                    if col >= max_images_per_row:
                        col = 0
                        row += 1

            # Añadir información de docentes y alumnos
            text_box = slide.shapes.add_textbox(
                Inches(6), Inches(5), Inches(4), Inches(2)
            )
            text_frame = text_box.text_frame
            p = text_frame.add_paragraph()
            p.text = "Docentes:"
            p.font.size = Pt(12)
            p.font.bold = True
            p.space_after = Pt(4)

            # Lista de docentes
            docentes_list = "\n".join(
                f"• {docente.nombre}" for docente in formulario_proyecto.docentes.all()
            )
            p = text_frame.add_paragraph()
            p.text = docentes_list
            p.font.size = Pt(12)
            p.space_after = Pt(6)

            p = text_frame.add_paragraph()
            p.text = f"Alumnos Participantes: {formulario_proyecto.alumnos}"
            p.font.size = Pt(12)
            p.font.bold = True

        # Agregar diapositiva con el problema
        slide_layout = presentation.slide_layouts[1]  # Título y contenido
        slide = presentation.slides.add_slide(slide_layout)
        title = slide.shapes.title
        content = slide.placeholders[1]
        title.text = "Problema"
        content.text = formulario_proyecto.problema
        content.text_frame.paragraphs[0].font.size = Pt(14)

        # Agregar diapositiva con la solución
        slide = presentation.slides.add_slide(slide_layout)
        title = slide.shapes.title
        content = slide.placeholders[1]
        title.text = "Solución"
        content.text = formulario_proyecto.solucion
        content.text_frame.paragraphs[0].font.size = Pt(14)

        # Guardar la presentación en un objeto BytesIO
        byte_io = BytesIO()
        presentation.save(byte_io)
        byte_io.seek(0)

        # Crear la respuesta HTTP
        response = HttpResponse(
            byte_io,
            content_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
        response["Content-Disposition"] = 'attachment; filename="presentacion.pptx"'

        return response

    def get(self, request, *args, **kwargs):
        cod_id = kwargs.get("pk")
        formulario_proyecto = get_object_or_404(FormularioProyectoFabLab, id=cod_id)
        return self.generate_ppt(formulario_proyecto)
