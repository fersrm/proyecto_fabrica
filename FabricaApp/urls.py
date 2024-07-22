from django.urls import path
from FabricaApp import views

urlpatterns = [
    path("", views.ProyectoInternoCreateView.as_view(), name="FabriCreate"),
    path("list/", views.ProyectoInternoListView.as_view(), name="FabriList"),
    path('ficha/<int:id>/', views.ProyectoInternoDetailView.as_view(), name='FabriDetail'),
    path("eliminar/<int:pk>/", views.ProyectoInternoDeleteView.as_view(), name="FabriDelete"),
    path("editar/<int:pk>/", views.ProyectoInternoUpdateView.as_view(), name="FabriUpdate"),
    path("ficha_fabrica/", views.ProyectoFabricaCreateView.as_view(), name="FabriFichaCreate"),
    path("ficha_fabrica/list/", views.ProyectoFabricaListView.as_view(), name="FabriFichaList"),
    path("ficha_fabrica/detalle/<int:id>/", views.ProyectoFabricaDetailView.as_view(), name="FabriFichaDetail"),
    path("ficha_fabrica/eliminar/<int:pk>/", views.ProyectoFabricaDeleteView.as_view(), name="FabriFichaDelete"),
    path("ficha_fabrica/editar/<int:pk>/", views.ProyectoFabricaUpdateView.as_view(), name="FabriFichaUpdate"),
]
