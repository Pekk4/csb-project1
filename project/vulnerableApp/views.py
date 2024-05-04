from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import connection

from .models import Message


# Create your views here.
def loginView(request):
  if request.method == 'POST':
    user = authenticate(
      request=request,
      username=request.POST['username'],
      password=request.POST['password']
    )

    if user is not None:
      login(request, user)

  return redirect('/')

def addView(request):
  if request.method == 'POST':
    user = User.objects.get(username=request.user)

    Message.objects.create(sender=user, content=request.POST['message'])

  return redirect('/')

def mainView(request):
  if not request.user.is_authenticated:
    return render(request, 'login.html')

  messages = Message.objects.all()

  return render(request, 'main.html', {'messages': messages})

def usermessagesView(request):
  if request.method == 'POST':
    with connection.cursor() as cursor:
      cursor.execute(f"SELECT content, time FROM vulnerableApp_message WHERE sender_id='{request.POST['user']}'")

      results = cursor.fetchall()
      messages = [{"content": result[0], "time": result[1]} for result in results]

  return render(request, 'messages.html', {'messages': messages})
