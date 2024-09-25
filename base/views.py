from django.shortcuts import render
from django.http import HttpResponse
from .models import Room


rooms = [
    {'id': 1, 'name': 'Python'},
    {'id': 2, 'name': 'c++'},
    {'id': 3, 'name': 'c#'}
]
# Create your views here.
def home(req):
    # return HttpResponse("<h1>Home page</h1>")
    room =Room.objects.all()
    print("🚀 ~ room:", room)
    return render(req,'base/home.html',{'rooms':rooms})

def room(req,pk):
    print("🚀 ~ pk:", pk)
    return render(req,"base/room.html")
