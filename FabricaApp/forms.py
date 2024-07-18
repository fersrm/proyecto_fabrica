from django import forms
from .models import FormularioProyectoInterno


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
            "potencial_comercial",
            "innovacion_proceso",
            "plan_trabajo",
            "trl_id",
            "docente_id",
            "empresa_id",
        )
        widgets = {
            "nombre_propuesta": forms.TextInput(
                attrs={"placeholder": "Nombre de la propuesta"}
            ),
            "area_vinculada": forms.TextInput(attrs={"placeholder": "Área vinculada"}),
            "problema": forms.Textarea(
                attrs={
                    "placeholder": "Descripción brevemente el problema presentado ",
                    "rows": 2,
                }
            ),
            "horas_disponibles": forms.NumberInput(
                attrs={"placeholder": "En horas ejemplo 2.5"}
            ),
            "rol_en_propuesta": forms.TextInput(
                attrs={"placeholder": "Rol en la propuesta"}
            ),
            "problema_oportunidad": forms.Textarea(
                attrs={
                    "placeholder": "Describir el problema que se busca resolver o la oportunidad que se busca abordar acotándolo a los alcances de la solución innovadora propuesta. Fundamentar quiénes se ven directamente afectados por este y entregar cifras, datos e información respaldada que permita cuantificar la magnitud del problema u oportunidad planteada (Papers, publicaciones, patentes, etc.). (Mínimo 5000/ Máximo 8000 caracteres)",
                    "rows": 7,
                }
            ),
            "solucion_innovadora": forms.Textarea(
                attrs={
                    "placeholder": "Describir la solución innovadora que se pretende desarrollar para resolver el problema o abordar la oportunidad identificada, fundamentando la agregación de valor respecto a la oferta actualmente disponible en el mercado y/o en los procesos productivos de las empresas/organizaciones, y la incertidumbre tecnológica asociada (Papers, publicaciones, patentes, etc.). (Mínimo 5000 caracteres) ",
                    "rows": 7,
                }
            ),
            "trl_id": forms.Select(
                attrs={"placeholder": "Nivel de madurez tecnológica"}
            ),
            "estado_avance": forms.TextInput(attrs={"placeholder": "Estado de avance"}),
            "potencial_comercial": forms.TextInput(
                attrs={"placeholder": "Potencial comercial"}
            ),
            "innovacion_proceso": forms.TextInput(
                attrs={"placeholder": "Innovación en el proceso"}
            ),
            "plan_trabajo": forms.TextInput(attrs={"placeholder": "Plan de trabajo"}),
            "docente_id": forms.Select(attrs={"placeholder": "Docente asociado"}),
            "empresa_id": forms.Select(attrs={"placeholder": "Empresa asociada"}),
        }
        labels = {
            "docente_id": "Docente Asociado",
            "empresa_id": "Empresa Asociada",
            "trl_id": "Nivel de madurez tecnológica",
        }
