from django.db import models
from django.contrib.auth.models import User
from utils.helpers import resize_image, crop_image
from .choices import ESTADO_POSTGRADO_CHOICES, ESTADO_PROYECTO_CHOICES
import uuid
import os


def upload_to_documentos(instance, filename):
    codigo_sir = instance.codigo_sir
    return f"fabrica/{codigo_sir}/documentos/{filename}"


def picture_path_fabrica(instance, filename):
    random_filename = str(uuid.uuid4())
    extension = os.path.splitext(filename)[1]
    codigo_sir = instance.ficha_fabrica.codigo_sir
    return f"fabrica/{codigo_sir}/img/{random_filename}{extension}"


def picture_path(instance, filename):
    random_filename = str(uuid.uuid4())
    extension = os.path.splitext(filename)[1]
    return f"fablab/img/{random_filename}{extension}"


############ DOCENTES ##############


class AreaAcademica(models.Model):
    area = models.CharField(max_length=100)

    class Meta:
        db_table = "area_academica"

    def __str__(self):
        return self.area


class Rol(models.Model):
    rol = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "rol"

    def __str__(self):
        return self.rol


class PostGrado(models.Model):
    titulo = models.CharField(max_length=200)
    estado = models.CharField(
        max_length=45, choices=ESTADO_POSTGRADO_CHOICES, default="TITULADO"
    )

    class Meta:
        db_table = "post_grados"

    def __str__(self):
        return self.estado


class Profesion(models.Model):
    nombre_titulo = models.CharField(max_length=45)
    licenciatura = models.CharField(max_length=60)
    estado = models.CharField(
        max_length=45, choices=ESTADO_POSTGRADO_CHOICES, default="TITULADO"
    )

    class Meta:
        db_table = "profesion"

    def __str__(self):
        return self.nombre_titulo


class Docente(models.Model):
    run = models.CharField(max_length=15)
    nombre = models.CharField(max_length=45)
    apellido_p = models.CharField(max_length=45)
    apellido_m = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    area_academica = models.ForeignKey(
        AreaAcademica, on_delete=models.CASCADE, default=1
    )
    roles = models.ManyToManyField(Rol)
    profesiones = models.ManyToManyField(Profesion)
    postgrados = models.ManyToManyField(PostGrado)

    class Meta:
        db_table = "docentes"

    def __str__(self):
        return self.nombre


############ EMPRESA #################


class Comuna(models.Model):
    comuna = models.CharField(max_length=45)

    class Meta:
        db_table = "comuna"

    def __str__(self):
        return self.comuna


class Rubro(models.Model):
    rubro = models.CharField(max_length=45)

    class Meta:
        db_table = "rubro"

    def __str__(self):
        return self.rubro


class Empresa(models.Model):
    rut_empresa = models.CharField(max_length=15)
    nombre_empresa = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE)

    class Meta:
        db_table = "empresas"

    def __str__(self):
        return self.nombre_empresa


class Cargo(models.Model):
    cargo_contraparte = models.CharField(max_length=45)

    class Meta:
        db_table = "cargo"

    def __str__(self):
        return self.cargo_contraparte


class ContraparteEmpresa(models.Model):
    run = models.CharField(max_length=15)
    nombre = models.CharField(max_length=45)
    apellido_p = models.CharField(max_length=45)
    apellido_m = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    cargo_id = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        db_table = "contraparte_empresa"

    def __str__(self):
        return self.nombre


############ PROYECTOS #################


class TRL(models.Model):
    trl_tipo = models.CharField(max_length=40)
    trl = models.CharField(max_length=70)

    class Meta:
        db_table = "trl"
        ordering = ["id"]

    def __str__(self):
        return self.trl_tipo


class Sede(models.Model):
    sede_nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.sede_nombre


###################################################
########## FORMULARIOS DE PROYECTOS ###############
###################################################

##### FORMULARIO PROYECTO FABRICA INTERNO CARLA ####


class FormularioProyectoInterno(models.Model):
    nombre_propuesta = models.CharField(max_length=200)
    area_vinculada = models.CharField(max_length=200)
    problema = models.TextField(max_length=8000)
    horas_disponibles = models.DecimalField(max_digits=10, decimal_places=1)
    rol_en_propuesta = models.CharField(max_length=200)
    problema_oportunidad = models.TextField(max_length=8000)
    solucion_innovadora = models.TextField(max_length=8000)
    estado_avance = models.TextField(max_length=8000)
    innovacion_proceso = models.TextField(max_length=8000, default="")
    registration_date = models.DateTimeField(auto_now_add=True)
    plan_trabajo = models.TextField(max_length=8000)  # pasar a archivo
    trl_id = models.ForeignKey(TRL, on_delete=models.CASCADE)
    docente_id = models.ForeignKey(Docente, on_delete=models.CASCADE)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=20, choices=ESTADO_PROYECTO_CHOICES, default="PROCESO"
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "formulario_proyecto_interno"

    def __str__(self):
        return self.nombre_propuesta


##### FORMULARIO PROYECTO FABRICA ANITA ####


class FormularioProyectoFabrica(models.Model):
    codigo_sir = models.CharField(max_length=25, unique=True)
    nombre_propuesta = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    registration_date = models.DateTimeField(auto_now_add=True)
    problema = models.TextField(max_length=8000)  # Descripcion del proyecto
    objetivo = models.TextField(max_length=5000)
    metodologia = models.TextField(max_length=8000)
    docente_id = models.ForeignKey(Docente, on_delete=models.CASCADE)
    bidireccionalidad = models.FileField(upload_to=upload_to_documentos)
    contribucion = models.FileField(upload_to=upload_to_documentos)
    carta_gantt = models.FileField(upload_to=upload_to_documentos)
    sede_id = models.ForeignKey(Sede, on_delete=models.CASCADE)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=20, choices=ESTADO_PROYECTO_CHOICES, default="PROCESO"
    )
    fondos = models.BooleanField(default=False)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "formulario_proyecto_fabrica"

    def __str__(self):
        return self.nombre_propuesta


class FabricaImage(models.Model):
    image = models.ImageField(upload_to=picture_path_fabrica)
    ficha_fabrica = models.ForeignKey(
        FormularioProyectoFabrica, related_name="images", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        super(FabricaImage, self).save(*args, **kwargs)

        if self.image and os.path.exists(self.image.path):
            resize_image(self.image.path, 500)
            crop_image(self.image.path, 500)


class FormularioProyectoFondos(models.Model):
    problema_oportunidad = models.TextField(max_length=8000)
    solucion_innovadora = models.TextField(max_length=8000)
    plan_trabajo = models.TextField(max_length=8000)
    potencial_comercializacion = models.TextField(max_length=8000)
    trl_id = models.ForeignKey(TRL, on_delete=models.CASCADE)
    proyecto = models.ForeignKey(
        FormularioProyectoFabrica,
        on_delete=models.CASCADE,
        related_name="fondos_proyecto",
    )

    class Meta:
        db_table = "formulario_proyecto_fondos"


##### FORMULARIO PROYECTO FABLAB MIGUEL #####


class FormularioProyectoFabLab(models.Model):
    nombre_propuesta = models.CharField(max_length=200)
    problema = models.TextField(max_length=8000)
    solucion = models.TextField(max_length=8000)
    alumnos = models.IntegerField()
    registration_date = models.DateTimeField(auto_now_add=True)
    docentes = models.ManyToManyField(Docente)
    trl_id = models.ForeignKey(TRL, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=20, choices=ESTADO_PROYECTO_CHOICES, default="PROCESO"
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


class FabLabImage(models.Model):
    image = models.ImageField(upload_to=picture_path)
    ficha_fablab = models.ForeignKey(
        FormularioProyectoFabLab, related_name="images", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        super(FabLabImage, self).save(*args, **kwargs)

        if self.image and os.path.exists(self.image.path):
            resize_image(self.image.path)
            crop_image(self.image.path)
