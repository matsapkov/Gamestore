from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from user.authentication import EmailAuthBackend
from django.contrib.auth.decorators import login_required
# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(request, username=email, password=password, backend=EmailAuthBackend())
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'user/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'user/registration.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': 'Gamestore - Profile', 'form': form}
    return render(request, 'user/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
