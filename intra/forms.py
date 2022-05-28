from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, \
    UserChangeForm, PasswordChangeForm

from .models import User


class IntraUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


class IntraUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'plaseholder': 'Enter your email',
        }))

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'plaseholder': 'Enter your first name',
        }))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'plaseholder': 'Enter your last name',
        }))
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'plaseholder': 'Enter your last username',
        }))

    # picture = forms.ImageField(
    #     widget=forms.FileInput(attrs={
    #         'class': 'form-control',
    #         'plaseholder': 'Upload image',
    #     }),
    # )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'description',
            'picture',
        ]
        field_classes = {"username": UsernameField}


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New Passowrd'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Conform new password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
