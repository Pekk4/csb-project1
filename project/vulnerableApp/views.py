from django.shortcuts import render, redirect


# Create your views here.
def loginView(request):
  if request.method == 'POST':
    print(request.POST)

  return render(request, 'login.html')