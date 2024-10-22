from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth
from django.urls import reverse
from user.models import User
from user.forms import UserLoginForm
from user.authentication import EmailAuthBackend
# Create your views here.
AUTH = EmailAuthBackend()


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = AUTH.authenticate(request, username=email, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'user/login.html', context)


def registration(request):
    context = {'title': 'Регистрация'}
    return render(request, 'user/registration.html', context)
