from django.contrib import admin
from .models import AuthUser


@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_verified", "created_at")
    search_fields = ("email",)
    list_filter = ("is_verified",)
    ordering = ("-created_at",)