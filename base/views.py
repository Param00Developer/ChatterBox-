from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

rooms =Room.objects.all()
# Create your views here.
def home(req):
    # return HttpResponse("<h1>Home page</h1>")
    return render(req,'base/home.html',{'rooms':rooms})

def room(req,pk):
    data=Room.objects.get(id=pk)
    return render(req,"base/room.html",{'room':data})

def createRoom(req):
    form=RoomForm()
    context={'form':form}
    return render(req,'base/room_form.html',context)