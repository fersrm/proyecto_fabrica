from django.contrib import admin
from .models import Profile, Position

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user_FK",)


class PositionAdmin(admin.ModelAdmin):
    list_display = ("user_position",)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Position, PositionAdmin)
