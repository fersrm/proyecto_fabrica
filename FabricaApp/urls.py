from django.urls import path
from FabricaApp import views

urlpatterns = [
    path("", views.ProyectoInternoCreateView.as_view(), name="FabriCreate"),
    path("list/", views.ProyectoInternoListView.as_view(), name="FabriList"),
    path('ficha/<int:id>/', views.ProyectoInternoDetailView.as_view(), name='FabriDetail'),
    path("eliminar/<int:pk>/", views.ProyectoInternoDeleteView.as_view(), name="FabriDelete"),
]
