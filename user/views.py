from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from user.forms import UserLoginForm
from user.authentication import EmailAuthBackend
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
    context = {'title': 'Регистрация'}
    return render(request, 'user/registration.html', context)
