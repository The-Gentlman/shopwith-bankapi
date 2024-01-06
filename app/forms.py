from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
