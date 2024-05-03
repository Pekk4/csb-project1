from django.urls import path

from .views import mainView, loginView, addView

urlpatterns = [
    path('', mainView, name='main'),
    path('login', loginView, name='login'),
    path('send', addView, name='send'),
]
