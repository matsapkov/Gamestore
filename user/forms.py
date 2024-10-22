from user.models import User
from django import forms


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


