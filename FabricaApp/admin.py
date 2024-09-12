from django.contrib import admin
from .models import (
    TRL,
    AreaAcademica,
    Docente,
    PostGrado,
    Profesion,
    Rol,
    FormularioProyectoFabrica,
    Sede,
)


# Register your models here.
class SedeAdmin(admin.ModelAdmin):
    list_display = ("sede_nombre",)


class TRLAdmin(admin.ModelAdmin):
    list_display = ("trl",)


class RolAdmin(admin.ModelAdmin):
    list_display = ("rol",)


class AreaAcademicaAdmin(admin.ModelAdmin):
    list_display = ("area",)


class DocenteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido_p", "email")


class PostGradoAdmin(admin.ModelAdmin):
    list_display = ("estado",)


class ProfesionAdmin(admin.ModelAdmin):
    list_display = ("nombre_titulo",)


################## FORMULARIOS ####################


class FormularioProyectoFabricaAdmin(admin.ModelAdmin):
    list_display = ("codigo_sir",)


admin.site.register(TRL, TRLAdmin)
admin.site.register(Rol, RolAdmin)
admin.site.register(AreaAcademica, AreaAcademicaAdmin)
admin.site.register(Docente, DocenteAdmin)
admin.site.register(PostGrado, PostGradoAdmin)
admin.site.register(Profesion, ProfesionAdmin)
admin.site.register(Sede, SedeAdmin)
admin.site.register(FormularioProyectoFabrica, FormularioProyectoFabricaAdmin)
