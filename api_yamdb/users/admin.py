from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
    #
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_unusable_password()
    #     if commit:
    #         user.save()
    #     return user

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2'),
        }),
    )

# admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)

