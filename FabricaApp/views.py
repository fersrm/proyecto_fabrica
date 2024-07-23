from .models import FormularioProyectoInterno, FormularioProyectoFabrica
from .forms import ProyectoInternoCreateForm, ProyectoFabricaCreateForm
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
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from core.mixins import PermitsPositionMixin

# para crear PDF
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Create your views here.


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


############################################


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


################################


class GeneratePdfNnaView(LoginRequiredMixin, View):
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
            img = Image(img_path, 2 * inch, 2 * inch)
            story.append(img)
            story.append(Spacer(1, 12))

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
