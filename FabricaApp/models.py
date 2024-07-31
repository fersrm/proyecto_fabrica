from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
import uuid
import os


ESTADO_CHOICES = [
    ("PROCESO", "En Proceso"),
    ("FINALIZADO", "Finalizado"),
    ("EN_REVISION", "En Revisión"),
]


def picture_path(instance, filename):
    random_filename = str(uuid.uuid4())
    extension = os.path.splitext(filename)[1]
    return f"proyectos/{random_filename}{extension}"


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
    titulo = models.BooleanField(default=False)
    estado = models.CharField(max_length=45)  # Titulado , Egresado , En curso

    class Meta:
        db_table = "post_grados"

    def __str__(self):
        return self.estado


class Profesion(models.Model):
    nombre_titulo = models.CharField(max_length=45)
    licenciatura = models.CharField(max_length=60)
    estado = models.CharField(max_length=45)

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


class TRL(models.Model):
    trl_tipo = models.CharField(max_length=40)
    trl = models.CharField(max_length=70)

    class Meta:
        db_table = "trl"
        ordering = ["id"]

    def __str__(self):
        return self.trl_tipo


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


####################################


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
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PROCESO")
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "formulario_proyecto_interno"

    def __str__(self):
        return self.nombre_propuesta


################################


class FormularioProyectoFabrica(models.Model):
    nombre_propuesta = models.CharField(max_length=200)
    problema = models.TextField(max_length=8000)
    solucion = models.TextField(max_length=8000)
    objetivos = models.TextField(max_length=8000)
    img = models.ImageField(upload_to=picture_path, null=True, blank=True)
    alumnos_ip = models.IntegerField()
    alumnos_cft = models.IntegerField()
    registration_date = models.DateTimeField(auto_now_add=True)
    docentes = models.ManyToManyField(Docente)
    trl_id = models.ForeignKey(TRL, on_delete=models.CASCADE)
    empresa_id = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PROCESO")
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        if self.pk:
            self.handle_old_image()

        super(FormularioProyectoFabrica, self).save(*args, **kwargs)

    def handle_old_image(self):
        try:
            old_profile = FormularioProyectoFabrica.objects.get(pk=self.pk)
            if self.img and old_profile.img != self.img:
                default_storage.delete(old_profile.img.path)
        except FormularioProyectoFabrica.DoesNotExist:
            pass

    class Meta:
        db_table = "formulario_proyecto_fabrica"

    def __str__(self):
        return self.nombre_propuesta


#################################


class FormularioProyectoFabLab(models.Model):
    nombre_propuesta = models.CharField(max_length=200)
    problema = models.TextField(max_length=8000)
    solucion = models.TextField(max_length=8000)
    alumnos = models.IntegerField()
    registration_date = models.DateTimeField(auto_now_add=True)
    docentes = models.ManyToManyField(Docente)
    trl_id = models.ForeignKey(TRL, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="PROCESO")
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


class FabLabImage(models.Model):
    image = models.ImageField(upload_to=picture_path)
    ficha_fablab = models.ForeignKey(
        FormularioProyectoFabLab, related_name="images", on_delete=models.CASCADE
    )
