from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)