from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Music

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
# Register your models here.
admin.site.register(Music)
