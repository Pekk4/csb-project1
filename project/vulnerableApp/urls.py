from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import mainView, loginView

urlpatterns = [
    path('', mainView, name='main'),
    path('login', loginView, name='login'),
]
