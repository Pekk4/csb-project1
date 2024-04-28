from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


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

def mainView(request):
  if not request.user.is_authenticated:
    return render(request, 'login.html')

  return render(request, 'main.html')
