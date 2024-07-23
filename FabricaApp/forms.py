from django import forms
from .models import FormularioProyectoInterno, FormularioProyectoFabrica


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
                attrs={"placeholder": "Nombre de la propuesta"}
            ),
            "area_vinculada": forms.TextInput(attrs={"placeholder": "Área vinculada"}),
            "problema": forms.Textarea(
                attrs={
                    "placeholder": "Descripción brevemente el problema presentado ",
                    "rows": 7,
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
                    "placeholder": """-.Describir la solución innovadora que se pretende desarrollar para resolver el problema o abordar la oportunidad identificada,fundamentando la agregación de valor respecto a la oferta actualmente disponible en el mercado y/o en los procesos productivos de las empresas/ organizaciones, y la incertidumbre tecnológica asociada (Papers, publicaciones, patentes, etc.). (Mínimo 5000 caracteres)                                                                     
-.Identificar y describir qué desarrollos tecnológicos y/o comerciales se han realizado recientemente a nivel nacional e internacional,     indicando las fuentes de información que lo respaldan (estado del arte), y en qué se diferencia la solución innovadora que se quiere llevar a cabo en el proyecto (Papers, publicaciones, patentes, etc.).                                                                           
-.Indicar si existe alguna consideración y/o restricción legal, normativa, sanitaria, propiedad intelectual, entre otros,que pueda afectar el desarrollo y/o implementación de la solución innovadora y cómo será abordada (N° Ley, Resolución, artículos, etc.).""",
                    "rows": 7,
                }
            ),
            "trl_id": forms.Select(
                attrs={"placeholder": "Nivel de madurez tecnológica"}
            ),
            "estado_avance": forms.Textarea(
                attrs={
                    "placeholder": "Descripción Estado de avance",
                    "rows": 7,
                }
            ),
            "innovacion_proceso": forms.Textarea(
                attrs={
                    "placeholder": """
                    INNOVACIÓN EN PRODUCTO (BIEN O SERVICIO)  

-.Caracterizar la oferta y demanda del mercado potencial del nuevo/mejorado producto (bien o servicio), acotado a los alcances de la solución innovadora propuesta. 
-.Caracterizar el segmento de mercado (clientes y/o usuarios potenciales) que estaría interesado en comprar y/o utilizar el nuevo/mejorado producto (bien o servicio) resultante de la propuesta. Describir el modelo de negocios que permitirá comercializar el nuevo o mejorado producto (bien o servicio) resultante de la propuesta, al cliente y/o usuario potencial identificado. 

                    INNOVACIÓN EN PROCESO 

-.Detalle cómo se implementará el nuevo o mejorado proceso obtenido en la empresa/organizaciones, antes del término de la propuesta. 
-.Describa y cuantifique cómo el nuevo o mejorado proceso impactará en el proceso productivo de la(s) empresa(s)/organizaciones vinculadas a la propuesta (reducción del costo y/o mejorará la calidad). """,
                    "rows": 7,
                }
            ),
            "plan_trabajo": forms.Textarea(
                attrs={
                    "placeholder": "Indique el objetivo general de la propuesta y objetivos específico",
                    "rows": 7,
                }
            ),
            "docente_id": forms.Select(attrs={"placeholder": "Docente asociado"}),
            "empresa_id": forms.Select(attrs={"placeholder": "Empresa asociada"}),
        }
        labels = {
            "problema": "Problema Presentado",
            "docente_id": "Docente Asociado",
            "empresa_id": "Empresa u organization Asociada",
            "trl_id": "Nivel de madurez tecnológica",
            "problema_oportunidad": "Problema u oportunidad",
            "innovacion_proceso": "Potencial de Comercialización y/o Implementación",
        }


class ProyectoFabricaCreateForm(forms.ModelForm):
    class Meta:
        model = FormularioProyectoFabrica
        fields = (
            "nombre_propuesta",
            "problema",
            "solucion",
            "objetivos",
            "img",
            "alumnos_ip",
            "alumnos_cft",
            "docentes",
            "trl_id",
            "empresa_id",
        )
        widgets = {
            "nombre_propuesta": forms.TextInput(
                attrs={"placeholder": "Nombre de la propuesta"}
            ),
            "problema": forms.Textarea(
                attrs={
                    "placeholder": "Descripción brevemente el problema presentado ",
                    "rows": 7,
                }
            ),
            "solucion": forms.Textarea(
                attrs={
                    "placeholder": """-.Describir la solución innovadora que se pretende desarrollar para resolver el problema o abordar la oportunidad identificada,fundamentando la agregación de valor respecto a la oferta actualmente disponible en el mercado y/o en los procesos productivos de las empresas/ organizaciones, y la incertidumbre tecnológica asociada (Papers, publicaciones, patentes, etc.). (Mínimo 5000 caracteres)                                                                     
-.Identificar y describir qué desarrollos tecnológicos y/o comerciales se han realizado recientemente a nivel nacional e internacional,     indicando las fuentes de información que lo respaldan (estado del arte), y en qué se diferencia la solución innovadora que se quiere llevar a cabo en el proyecto (Papers, publicaciones, patentes, etc.).                                                                           
-.Indicar si existe alguna consideración y/o restricción legal, normativa, sanitaria, propiedad intelectual, entre otros,que pueda afectar el desarrollo y/o implementación de la solución innovadora y cómo será abordada (N° Ley, Resolución, artículos, etc.).""",
                    "rows": 7,
                }
            ),
            "objetivos": forms.Textarea(
                attrs={
                    "placeholder": "Objetivos",
                    "rows": 7,
                }
            ),
            "trl_id": forms.Select(
                attrs={"placeholder": "Nivel de madurez tecnológica"}
            ),
            "docente_id": forms.Select(attrs={"placeholder": "Docente asociado"}),
            "empresa_id": forms.Select(attrs={"placeholder": "Empresa asociada"}),
        }
        labels = {
            "problema": "Problema Presentado",
            "docente_id": "Docentes Asociados",
            "empresa_id": "Empresa u organization Asociada",
            "trl_id": "Nivel de madurez tecnológica",
        }
