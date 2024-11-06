from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from user.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from user.authentication import EmailAuthBackend
from products.models import Basket
from django.views.generic.edit import CreateView, UpdateView
from user.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from common.views import TitleMixin
# Create your views here.


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    template_name = 'user/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:login')
    success_message = 'You have successfully registered.'
    title = 'Gamestore - Registration'


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
    context = {'form': form,
               'title': 'Gamestore - Login'
               }
    return render(request, 'user/login.html', context)


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/profile.html'
    title = 'Gamestore - Profile'

    def get_success_url(self):
        return reverse_lazy('user:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

# class UserLoginView(LoginView):
#     template_name = 'user/login.html'
#     form_class = UserLoginForm

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('user:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     baskets = Basket.objects.filter(user=request.user)
#
#     context = {'title': 'Gamestore - Profile',
#                'form': form,
#                'baskets': Basket.objects.filter(user=request.user),
#                }
#     return render(request, 'user/profile.html', context)

