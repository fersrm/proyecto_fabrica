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
)


# Register your models here.
class TRLAdmin(admin.ModelAdmin):
    list_display = ("trl",)


admin.site.register(TRL, TRLAdmin)


class RolAdmin(admin.ModelAdmin):
    list_display = ("rol",)


admin.site.register(Rol, RolAdmin)


class ComunaAdmin(admin.ModelAdmin):
    list_display = ("comuna", "id")


admin.site.register(Comuna, ComunaAdmin)


class AreaAcademicaAdmin(admin.ModelAdmin):
    list_display = ("area",)


admin.site.register(AreaAcademica, AreaAcademicaAdmin)


class DocenteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "apellido_p", "email")


admin.site.register(Docente, DocenteAdmin)


class PostGradoAdmin(admin.ModelAdmin):
    list_display = ("estado",)


admin.site.register(PostGrado, PostGradoAdmin)


class ProfesionAdmin(admin.ModelAdmin):
    list_display = ("nombre_titulo",)


admin.site.register(Profesion, ProfesionAdmin)


class RubroAdmin(admin.ModelAdmin):
    list_display = ("rubro",)


admin.site.register(Rubro, RubroAdmin)


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("nombre_empresa",)


admin.site.register(Empresa, EmpresaAdmin)


class FormularioProyectoInternoAdmin(admin.ModelAdmin):
    list_display = ("nombre_propuesta",)


admin.site.register(FormularioProyectoInterno, FormularioProyectoInternoAdmin)


class CargoAdmin(admin.ModelAdmin):
    list_display = ("cargo_contraparte",)


admin.site.register(Cargo, CargoAdmin)


class ContraparteEmpresaAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido_p",
        "email",
    )


admin.site.register(ContraparteEmpresa, ContraparteEmpresaAdmin)
