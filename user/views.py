from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from user.authentication import EmailAuthBackend
from products.models import Basket
from django.views.generic.edit import CreateView
from user.models import User
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


class UserRegistrationView(CreateView):
    model = User
    template_name = 'user/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('index')


@login_required
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

    baskets = Basket.objects.filter(user=request.user)

    context = {'title': 'Gamestore - Profile',
               'form': form,
               'baskets': Basket.objects.filter(user=request.user),
               }
    return render(request, 'user/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
