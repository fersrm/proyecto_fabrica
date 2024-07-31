from django.contrib import admin
from .models import (
    TRL,
    Comuna,
    AreaAcademica,
    Docente,
    PostGrado,
    Profesion,
    Rubro,
    Empresa,
    FormularioProyectoInterno,
    Cargo,
    ContraparteEmpresa,
    Rol,
    FormularioProyectoFabLab,
)


# Register your models here.
class TRLAdmin(admin.ModelAdmin):
    list_display = ("trl",)


class RolAdmin(admin.ModelAdmin):
    list_display = ("rol",)


class ComunaAdmin(admin.ModelAdmin):
    list_display = ("comuna", "id")


class AreaAcademicaAdmin(admin.ModelAdmin):
    list_display = ("area",)


class DocenteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido_p", "email")


class PostGradoAdmin(admin.ModelAdmin):
    list_display = ("estado",)


class ProfesionAdmin(admin.ModelAdmin):
    list_display = ("nombre_titulo",)


class RubroAdmin(admin.ModelAdmin):
    list_display = ("rubro",)


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nombre_empresa",)


class FormularioProyectoInternoAdmin(admin.ModelAdmin):
    list_display = ("nombre_propuesta",)


class CargoAdmin(admin.ModelAdmin):
    list_display = ("cargo_contraparte",)


class ContraparteEmpresaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido_p",
        "email",
    )


################## FORMULARIOS
class FormularioProyectoFabLabAdmin(admin.ModelAdmin):
    list_display = ("nombre_propuesta",)


admin.site.register(TRL, TRLAdmin)
admin.site.register(Rol, RolAdmin)
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(AreaAcademica, AreaAcademicaAdmin)
admin.site.register(Docente, DocenteAdmin)
admin.site.register(PostGrado, PostGradoAdmin)
admin.site.register(Profesion, ProfesionAdmin)
admin.site.register(Rubro, RubroAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(FormularioProyectoInterno, FormularioProyectoInternoAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(ContraparteEmpresa, ContraparteEmpresaAdmin)
admin.site.register(FormularioProyectoFabLab, FormularioProyectoFabLabAdmin)
