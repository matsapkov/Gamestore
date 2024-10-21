from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth
from django.urls import reverse
from user.models import User
from user.forms import UserLoginForm

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        print('--------------------------------------------------')
        if form.is_valid():
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # email = request.POST['email']
            # password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'user/login.html', context)




def registration(request):
    context = {'title': 'Регистрация'}
    return render(request, 'user/registration.html', context)
