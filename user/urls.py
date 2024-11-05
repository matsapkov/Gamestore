from django.urls import path
from user.views import login, profile, logout, UserRegistrationView

app_name = 'user'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
]

