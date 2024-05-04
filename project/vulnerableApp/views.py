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
      param = [request.POST['user']]
      cursor.execute(f"SELECT content, time FROM vulnerableApp_message WHERE sender_id=%s", param)

      results = cursor.fetchall()
      messages = [{"content": result[0], "time": result[1]} for result in results]

  return render(request, 'usermessages.html', {'messages': messages})

def xssmessagesView(request):
  if not request.user.is_authenticated:
    return render(request, 'login.html')

  messages = Message.objects.all()

  return render(request, 'xssmessages.html', {'messages': messages})

def adminView(request):
  if request.user.is_superuser:
    users = User.objects.all()
    users = users.exclude(id=users.first().id)

    return render(request, 'adminview.html', {'users': users})

  return redirect('/')

def deleteusersView(request):
  if request.user.is_superuser:
    if request.method == 'GET':
      user = request.GET['username']

      User.delete(User.objects.get(username=user))

    return redirect('/adminview')

  return redirect('/')
