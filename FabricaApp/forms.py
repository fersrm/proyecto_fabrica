from django import forms
from django.core.exceptions import ValidationError
from .models import (
    FormularioProyectoFabrica,
    FabricaImage,
    FormularioProyectoFondos,
)
from .form_config import PLACEHOLDERS, CLASSES, FORMATOS
from datetime import date
from unidecode import unidecode
import os


##############################################
##### FORMULARIO PROYECTO FABRICA ######
##############################################


class ProyectoFabricaCreateForm(forms.ModelForm):

    codigo_sir = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": PLACEHOLDERS["codigo_sir"],
                "class": CLASSES["textinput"],
            }
        ),
    )

    class Meta:
        model = FormularioProyectoFabrica
        fields = (
            "codigo_sir",
            "nombre_propuesta",
            "sede_id",
            "fecha_inicio",
            "empresa",
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
                    "rows": 4,
                    "class": CLASSES["textarea"],
                }
            ),
            "objetivo": forms.Textarea(
                attrs={
                    "placeholder": PLACEHOLDERS["objetivo"],
                    "rows": 5,
                    "class": CLASSES["textarea"],
                }
            ),
            "metodologia": forms.Textarea(
                attrs={
                    "placeholder": PLACEHOLDERS["metodologia"],
                    "rows": 5,
                    "class": CLASSES["textarea"],
                }
            ),
            "docente_id": forms.Select(
                attrs={
                    "placeholder": PLACEHOLDERS["docente_id"],
                    "class": CLASSES["select"],
                }
            ),
            "empresa": forms.TextInput(
                attrs={
                    "placeholder": PLACEHOLDERS["empresa"],
                    "class": CLASSES["textinput"],
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
            "bidireccionalidad": "Bidireccionalidad (Datos Docentes y Estudiantes)",
            "contribucion": "Contribución (Datos Empresa y/o Beneficiario)",
            "sede_id": "Sede",
            "empresa": "Empresa u organización asociada",
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

        return cleaned_data

    def clean_problema(self):
        problema = self.cleaned_data.get("problema")
        if len(problema) < 100:
            raise forms.ValidationError("El texto debe tener al menos 100 caracteres.")
        return problema

    def clean_objetivo(self):
        objetivo = self.cleaned_data.get("objetivo")
        if len(objetivo) < 100:
            raise forms.ValidationError("El texto debe tener al menos 100 caracteres.")
        return objetivo

    def clean_metodologia(self):
        metodologia = self.cleaned_data.get("metodologia")
        if len(metodologia) < 100:
            raise forms.ValidationError("El texto debe tener al menos 100 caracteres.")
        return metodologia

    def clean_fecha_inicio(self):
        fecha_inicio = self.cleaned_data.get("fecha_inicio")

        if fecha_inicio and fecha_inicio > date.today():
            raise forms.ValidationError(
                "La fecha de inicio no puede ser mayor a la fecha actual."
            )

        return fecha_inicio

    def clean_empresa(self):
        empresa = self.cleaned_data.get("empresa")

        if isinstance(empresa, str):
            empresa = unidecode(empresa.upper().strip())

        return empresa


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

    def clean_problema_oportunidad(self):
        problema_oportunidad = self.cleaned_data.get("problema_oportunidad")
        if problema_oportunidad and len(problema_oportunidad) < 5000:
            raise forms.ValidationError(
                'El campo "Problema u oportunidad" debe tener al menos 5000 caracteres.'
            )
        return problema_oportunidad

    def clean_solucion_innovadora(self):
        solucion_innovadora = self.cleaned_data.get("solucion_innovadora")
        if solucion_innovadora and len(solucion_innovadora) < 5000:
            raise forms.ValidationError(
                'El campo "Solución innovadora" debe tener al menos 5000 caracteres.'
            )
        return solucion_innovadora

    def clean_potencial_comercializacion(self):
        potencial_comercializacion = self.cleaned_data.get("potencial_comercializacion")
        if potencial_comercializacion and len(potencial_comercializacion) < 5000:
            raise forms.ValidationError(
                'El campo "Potencial de comercialización" debe tener al menos 5000 caracteres.'
            )
        return potencial_comercializacion

    def clean_plan_trabajo(self):
        plan_trabajo = self.cleaned_data.get("plan_trabajo")
        if plan_trabajo and len(plan_trabajo) < 2000:
            raise forms.ValidationError(
                'El campo "Plan de trabajo" debe tener al menos 2000 caracteres.'
            )
        return plan_trabajo


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


########## FORMULARIO DE IMÁGENES FABRICA ########
class ImageFabricaForm(forms.ModelForm):
    image = MultipleFileField(label="Incluir imágenes (4 imágenes)", required=False)

    class Meta:
        model = FabricaImage
        fields = [
            "image",
        ]
