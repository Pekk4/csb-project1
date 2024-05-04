from django.urls import path

from .views import mainView, loginView, addView, usermessagesView, xssmessagesView

urlpatterns = [
    path('', mainView, name='main'),
    path('login', loginView, name='login'),
    path('send', addView, name='send'),
    path('usermessages', usermessagesView, name='usermessages'),
    path('messages', xssmessagesView, name='messages'),
]
