from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from UsuarioApp.models import Profile
from FabricaApp.models import FormularioProyectoInterno, FormularioProyectoFabrica

# Create your views here.


class HomeView(LoginRequiredMixin, ListView):
    model = User
    template_name = "pages/index.html"

    def get_queryset(self):
        last_connected_users = User.objects.filter(
            Q(last_login__isnull=False)
        ).order_by("-last_login")[:5]
        return last_connected_users

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Agrega los usuarios activos al contexto
        recent_activity_cutoff = timezone.now() - timezone.timedelta(minutes=2)
        active_users = Profile.objects.filter(
            last_activity__gte=recent_activity_cutoff
        ).values_list("user_FK_id", flat=True)
        context["active_users"] = active_users

        # Agrega el recuento
        proyecto_count = FormularioProyectoInterno.objects.count()
        latest_proyecto = FormularioProyectoInterno.objects.order_by(
            "-registration_date"
        ).first()
        latest_registration_date = (
            latest_proyecto.registration_date if latest_proyecto else None
        )
        latest_registration_user = (
            latest_proyecto.user_id.username
            if latest_proyecto and latest_proyecto.user_id
            else None
        )

        context["proyecto_count"] = proyecto_count
        context["latest_registration_date"] = latest_registration_date
        context["latest_registration_user"] = latest_registration_user

        # Agrega el recuento
        proyecto_count_ficha = FormularioProyectoFabrica.objects.count()
        latest_proyecto_ficha = FormularioProyectoFabrica.objects.order_by(
            "-registration_date"
        ).first()
        latest_registration_date_ficha = (
            latest_proyecto_ficha.registration_date if latest_proyecto_ficha else None
        )
        latest_registration_user_ficha = (
            latest_proyecto_ficha.user_id.username
            if latest_proyecto_ficha and latest_proyecto_ficha.user_id
            else None
        )

        context["proyecto_count_ficha"] = proyecto_count_ficha
        context["latest_registration_date_ficha"] = latest_registration_date_ficha
        context["latest_registration_user_ficha"] = latest_registration_user_ficha

        return context
