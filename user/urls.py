from django.urls import path
from user.views import UserRegistrationView, UserProfileView, login, LogoutView
from django.contrib.auth.decorators import login_required


app_name = 'user'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

