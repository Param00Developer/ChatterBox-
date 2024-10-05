from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import  Q
from .models import Room,Topic,Message
from .forms import RoomForm

rooms =Room.objects.all()
# Create your views here.
def home(req):
    q=req.GET.get('q') if req.GET.get('q') else ''
    # rooms=Room.objects.filter(topic__name__icontains=q)# checks  if the name of the topic contains the query
    # Searching with Q function
    rooms=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) |  Q(description__icontains=q))
    topics=Topic.objects.all()
    # room_messages=Message.objects.all()
    # get messages based on individual rooms
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'room_count':rooms.count(),'room_messages':room_messages}
    return render(req,'base/home.html',context)

def room(req,pk):
    data=Room.objects.get(id=pk)
    room_messages=data.message_set.all()
    participants=data.participants.all()
    if req.method=='POST':
        Message.objects.create(user=req.user,room=data,body=req.POST.get('body'))
        data.participants.add(req.user)
        return redirect('room',pk=data.id)
    print("🚀 ~ room_messages:", room_messages)
    context={'room':data,'room_messages':room_messages,'participants':participants}
    return render(req,"base/room.html",context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def updateRoom(req,pk):
    room=Room.objects.get(id=pk)
    print(f"User:{req.user}")
    if req.user !=room.host:
        return HttpResponse("Not  allowed!!!")

    form=RoomForm(instance=room)
    if req.method=='POST':
        form=RoomForm(req.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(req,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(req,pk):
    room=Room.objects.get(id=pk)
    if req.user !=room.host:
        return HttpResponse("Not  allowed!!!")
    if req.method=='POST':
        room.delete()
        return redirect('home')
    return render(req,'base/delete.html',{'obj':room,'prev_url':req.META['HTTP_REFERER']})

@login_required(login_url='login')
def deleteMessage(req,pk):
    msg=Message.objects.get(id=pk)
    if req.user !=msg.user:
        return HttpResponse("Not  allowed!!!")
    if req.method=='POST':
        msg.delete()
        return redirect('home')
    return render(req,'base/delete.html',{'obj':msg})

def loginPage(req):
    page='Login'
    if req.user.is_authenticated:
        return redirect('home')
    if  req.method=='POST':
        username=req.POST.get('username')
        password=req.POST.get('password')
        try:
            user=User.objects.get(username=username)
            print("🚀 ~ user:1", user)
            user=authenticate(req,username=username,password=password)
            print("🚀 ~ user:2", user)
            if  user is not None:
                login(req,user)
                return redirect('home')
            else:
                messages.error(req,'Username or Password is wrong')
        except:
            messages.error(req,'User not found')

    context={'page':page}
    return render(req,'base/register.html',context)

def logoutUser(req):
    logout(req)
    return redirect('home')

def registerUser(req):
    form=UserCreationForm()
    if req.method=='POST':
        try:
            form=UserCreationForm(req.POST)
            if form.is_valid():
                user=form.save(commit=False)
                user.username=user.username.lower()
                user.save()
                login(req,user)
                return redirect('home')
            else:
                messages.error(req,"Some Error occurred ..")
        except Exception as e:
            print(e)
            messages.error(req,e.message)
    
    return render(req,'base/register.html',{'form':form})