from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User


# -----------------------------------------------------------------------------
# User
# -----------------------------------------------------------------------------
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
	form = CustomUserChangeForm
	list_display = UserAdmin.list_display + ('is_superuser', )
	readonly_fields = UserAdmin.readonly_fields
	list_editable = ('is_staff', 'is_superuser', )
