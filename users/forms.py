from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
