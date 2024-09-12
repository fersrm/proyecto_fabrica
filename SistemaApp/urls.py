from django.urls import path
from SistemaApp import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="Home"),
    path(
        "descargar_proyectos_fabrica/",
        views.DescargarProyectosFabricaView.as_view(),
        name="descargar_proyectos_fabrica",
    ),
]
