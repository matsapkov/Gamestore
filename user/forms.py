from user.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'email',
        'id': 'email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'password',
        'id': 'password'
    }))

    class Meta:
        model = User
        fields = ('email', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'firstName',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'lastName',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'username',
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'email',
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'address',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'confirmPassword',
    }))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'address', 'password1', 'password2')
