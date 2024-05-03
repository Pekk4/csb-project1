from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
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
