from django.urls import path
from FabricaApp import views

urlpatterns = [
    path("", views.ProyectoInternoCreateView.as_view(), name="FabriCreate"),
    path("list/", views.ProyectoInternoListView.as_view(), name="FabriList"),
]
