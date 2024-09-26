from django.shortcuts import render,redirect
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
    if req.method=="POST":
        print("Data to be posted ::",req.POST)
        form=RoomForm(req.POST)
        if(form.is_valid()):
            form.save()
            print("Data saved")
            return redirect('home')
    context={'form':form}
    return render(req,'base/room_form.html',context)

def updateRoom(req,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if req.method=='POST':
        form=RoomForm(req.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(req,'base/room_form.html',context)

def deleteRoom(req,pk):
    room=Room.objects.get(id=pk)
    print(req.method)
    if req.method=='POST':
        room.delete()
        room.save()
        return redirect('home')
    return render(req,'base/delete.html',{'obj':room})
