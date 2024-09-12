from django.urls import path
from FabricaApp import views

urlpatterns = [
    path(
        "ficha_fabrica/",
        views.ProyectoFabricaCreateView.as_view(),
        name="FabriFichaCreate",
    ),
    path(
        "ficha_fabrica/list/",
        views.ProyectoFabricaListView.as_view(),
        name="FabriFichaList",
    ),
    path(
        "ficha_fabrica/detalle/<int:id>/",
        views.ProyectoFabricaDetailView.as_view(),
        name="FabriFichaDetail",
    ),
    path(
        "ficha_fabrica/eliminar/<int:pk>/",
        views.ProyectoFabricaDeleteView.as_view(),
        name="FabriFichaDelete",
    ),
    path(
        "ficha_fabrica/editar/<int:pk>/",
        views.ProyectoFabricaUpdateView.as_view(),
        name="FabriFichaUpdate",
    ),
    path(
        "ficha_fabrica/generar_pdf/<pk>/",
        views.PdfView.as_view(),
        name="GeneratePdf",
    ),
]
