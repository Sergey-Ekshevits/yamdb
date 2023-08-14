from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role',
                       'bio', 'password1', 'password2', 'is_staff'),
        }),
    )
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role',
                       'bio', 'is_staff'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
