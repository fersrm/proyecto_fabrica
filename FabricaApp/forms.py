from django import forms
from django.core.exceptions import ValidationError
from .models import (
    FormularioProyectoInterno,
    FormularioProyectoFabrica,
    FormularioProyectoFabLab,
    FabLabImage,
    FabricaImage,
    FormularioProyectoFondos,
)
from .form_config import PLACEHOLDERS, CLASSES, FORMATOS
from datetime import date
import os


##############################################
##### FORMULARIO PROYECTO FABRICA CARLA ######
##############################################


class ProyectoInternoCreateForm(forms.ModelForm):
    class Meta:
        model = FormularioProyectoInterno
        fields = (
            "nombre_propuesta",
            "area_vinculada",
            "problema",
            "horas_disponibles",
            "rol_en_propuesta",
            "problema_oportunidad",
            "solucion_innovadora",
            "estado_avance",
            "innovacion_proceso",
            "plan_trabajo",
            "trl_id",
            "docente_id",
            "empresa_id",
        )
        widgets = {
            "nombre_propuesta": forms.TextInput(
                attrs={"placeholder": PLACEHOLDERS["nombre_propuesta"]}
            ),
            "area_vinculada": forms.TextInput(
                attrs={"placeholder": PLACEHOLDERS["area_vinculada"]}
            ),
            "problema": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["problema"], "rows": 7}
            ),
            "horas_disponibles": forms.NumberInput(
                attrs={"placeholder": PLACEHOLDERS["horas_disponibles"]}
            ),
            "rol_en_propuesta": forms.TextInput(
                attrs={"placeholder": PLACEHOLDERS["rol_en_propuesta"]}
            ),
            "problema_oportunidad": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["problema_oportunidad"], "rows": 7}
            ),
            "solucion_innovadora": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["solucion_innovadora"], "rows": 7}
            ),
            "trl_id": forms.Select(attrs={"placeholder": PLACEHOLDERS["trl_id"]}),
            "estado_avance": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["estado_avance"], "rows": 7}
            ),
            "innovacion_proceso": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["innovacion_proceso"], "rows": 7}
            ),
            "plan_trabajo": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["plan_trabajo"], "rows": 7}
            ),
            "docente_id": forms.Select(
                attrs={"placeholder": PLACEHOLDERS["docente_id"]}
            ),
            "empresa_id": forms.Select(
                attrs={"placeholder": PLACEHOLDERS["empresa_id"]}
            ),
        }
        labels = {
            "problema": "Problema Presentado",
            "docente_id": "Docente Asociado",
            "empresa_id": "Empresa u organization Asociada",
            "trl_id": "Nivel de madurez tecnológica",
            "problema_oportunidad": "Problema u oportunidad",
            "innovacion_proceso": "Potencial de Comercialización y/o Implementación",
        }


##############################################
##### FORMULARIO PROYECTO FABRICA ANITA ######
##############################################


class ProyectoFabricaCreateForm(forms.ModelForm):
    class Meta:
        model = FormularioProyectoFabrica
        fields = (
            "codigo_sir",
            "nombre_propuesta",
            "sede_id",
            "fecha_inicio",
            "empresa_id",
            "problema",
            "objetivo",
            "metodologia",
            "docente_id",
            "bidireccionalidad",
            "contribucion",
            "carta_gantt",
            "fondos",
        )
        widgets = {
            "codigo_sir": forms.TextInput(
                attrs={
                    "placeholder": PLACEHOLDERS["codigo_sir"],
                    "class": CLASSES["textinput"],
                }
            ),
            "nombre_propuesta": forms.TextInput(
                attrs={
                    "placeholder": PLACEHOLDERS["nombre_propuesta"],
                    "class": CLASSES["textinput"],
                }
            ),
            "fecha_inicio": forms.DateInput(
                attrs={"type": "date", "class": CLASSES["textinput"]}
            ),
            "problema": forms.Textarea(
                attrs={
                    "placeholder": PLACEHOLDERS["problema"],
                    "rows": 7,
                    "class": CLASSES["textarea"],
                }
            ),
            "objetivo": forms.Textarea(
                attrs={
                    "placeholder": PLACEHOLDERS["objetivo"],
                    "rows": 7,
                    "class": CLASSES["textarea"],
                }
            ),
            "metodologia": forms.Textarea(
                attrs={
                    "placeholder": PLACEHOLDERS["metodologia"],
                    "rows": 7,
                    "class": CLASSES["textarea"],
                }
            ),
            "docente_id": forms.Select(
                attrs={
                    "placeholder": PLACEHOLDERS["docente_id"],
                    "class": CLASSES["select"],
                }
            ),
            "empresa_id": forms.Select(
                attrs={
                    "placeholder": PLACEHOLDERS["empresa_id"],
                    "class": CLASSES["select"],
                }
            ),
            "sede_id": forms.Select(
                attrs={"placeholder": "Sede", "class": CLASSES["select"]}
            ),
            "carta_gantt": forms.FileInput(attrs={"accept": FORMATOS["excel"]}),
            "bidireccionalidad": forms.FileInput(attrs={"accept": FORMATOS["excel"]}),
            "contribucion": forms.FileInput(attrs={"accept": FORMATOS["excel"]}),
        }
        labels = {
            "codigo_sir": "Id de proyecto",
            "nombre_propuesta": "Título del Proyecto",
            "problema": "Introducción o Contexto del Problema",
            "objetivo": "Objetivo del Proyecto",
            "metodologia": "Metodología",
            "docente_id": "Docente líder",
            "bidireccionalidad": "Bidireccionalidad",
            "contribucion": "Contribución",
            "sede_id": "Sede",
            "empresa_id": "Empresa u organización asociada",
            "carta_gantt": "Carta Gantt",
            "fondos": "Postula a fondos concursables",
        }

    def clean(self):
        cleaned_data = super().clean()

        # Validaciones para archivos
        carta_gantt = cleaned_data.get("carta_gantt")
        bidireccionalidad = cleaned_data.get("bidireccionalidad")
        contribucion = cleaned_data.get("contribucion")

        documents = {
            "carta_gantt": carta_gantt,
            "bidireccionalidad": bidireccionalidad,
            "contribucion": contribucion,
        }

        for field_name, document in documents.items():
            if document:
                if not document.name.endswith(".xlsx"):
                    self.add_error(
                        field_name, "El archivo debe ser de formato Excel (xlsx)."
                    )
                max_size = 5 * 1024 * 1024  # 5 MB
                if document.size > max_size:
                    self.add_error(
                        field_name,
                        "El tamaño del archivo no puede ser mayor a 5 megabytes.",
                    )

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get("fecha_inicio")

        if fecha_inicio and fecha_inicio > date.today():
            raise forms.ValidationError(
                "La fecha de inicio no puede ser mayor a la fecha actual."
            )

        return fecha_inicio


#### FORMULARIO PROYECTO FABRICA FONDOS ####


class ProyectoFabricaFondosCreateForm(forms.ModelForm):
    class Meta:
        model = FormularioProyectoFondos
        fields = (
            "problema_oportunidad",
            "solucion_innovadora",
            "potencial_comercializacion",
            "plan_trabajo",
            "trl_id",
        )

        widgets = {
            "problema_oportunidad": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["problema_oportunidad"], "rows": 7}
            ),
            "solucion_innovadora": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["solucion_innovadora"], "rows": 7}
            ),
            "potencial_comercializacion": forms.Textarea(
                attrs={
                    "placeholder": PLACEHOLDERS["potencial_comercializacion"],
                    "rows": 7,
                }
            ),
            "plan_trabajo": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["plan_trabajo"], "rows": 7}
            ),
            "trl_id": forms.Select(attrs={"placeholder": PLACEHOLDERS["trl_id"]}),
        }

        labels = {
            "solucion_innovadora": "Solución innovadora",
            "problema_oportunidad": "Problema u oportunidad",
            "potencial_comercializacion": "Potencial de comercialización",
            "trl_id": "Nivel de madurez tecnológica",
        }


##############################################
##### FORMULARIO PROYECTO FABLAB #############
##############################################


class ProyectoFabLabCreateForm(forms.ModelForm):
    class Meta:
        model = FormularioProyectoFabLab
        fields = (
            "nombre_propuesta",
            "problema",
            "solucion",
            "alumnos",
            "docentes",
            "trl_id",
        )
        widgets = {
            "nombre_propuesta": forms.TextInput(
                attrs={"placeholder": PLACEHOLDERS["nombre_propuesta"]}
            ),
            "problema": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["problema"], "rows": 7}
            ),
            "solucion": forms.Textarea(
                attrs={"placeholder": PLACEHOLDERS["solucion_innovadora"], "rows": 7}
            ),
            "trl_id": forms.Select(attrs={"placeholder": PLACEHOLDERS["trl_id"]}),
            "docentes": forms.SelectMultiple(
                attrs={"placeholder": PLACEHOLDERS["docente_id"]}
            ),
        }
        labels = {
            "problema": "Problema Presentado",
            "docentes": "Docentes Asociados",
            "trl_id": "Nivel de madurez tecnológica",
        }

    def clean_docentes(self):
        docentes = self.cleaned_data.get("docentes")
        if docentes is None or len(docentes) == 0:
            raise forms.ValidationError("Debe seleccionar al menos un docente.")

        return docentes


#############################################
######  MANEJO DE MULTIPLES IMÁGENES #######
#############################################


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.update({"accept": FORMATOS["img"]})
        super().__init__(attrs)


def validate_file_extension(file_name):
    allowed_extensions = [".webp", ".png", ".jpg", ".jpeg"]
    extension = os.path.splitext(file_name)[1].lower()
    if extension not in allowed_extensions:
        raise ValidationError(
            f"El archivo '{file_name}' no tiene un formato permitido. Solo se permiten archivos .webp, .png y .jpg."
        )


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            if len(data) != 4:
                raise ValidationError("Deben ser 4 imágenes.")

            # Validar el formato de cada archivo
            result = []
            for d in data:
                if d:
                    validate_file_extension(d.name)
                    result.append(single_file_clean(d, initial))

        else:
            validate_file_extension(data.name)
            result = single_file_clean(data, initial)

        return result


#################################################
#### FORMULARIOS PARA LAS IMÁGENES ##############
#################################################

########## FORMULARIO DE IMÁGENES FABLAB ########


class ImageForm(forms.ModelForm):
    image = MultipleFileField(label="Incluir imágenes (4 imágenes)", required=False)

    class Meta:
        model = FabLabImage
        fields = [
            "image",
        ]


########## FORMULARIO DE IMÁGENES FABRICA ########
class ImageFabricaForm(forms.ModelForm):
    image = MultipleFileField(label="Incluir imágenes (4 imágenes)", required=False)

    class Meta:
        model = FabricaImage
        fields = [
            "image",
        ]
