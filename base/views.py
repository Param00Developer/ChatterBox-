from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(req):
    # return HttpResponse("<h1>Welcome to home route </h1>")
    return render(req,'home.html')
def dashboard(req):
    # return HttpResponse("<h1>Welcome to dashboard route </h1>")
    return render(req,'dashboard.html')
def empty(req):
    return HttpResponse("</h2 color='red' >Empty page</h2>")