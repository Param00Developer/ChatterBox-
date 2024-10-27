import json
import random
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import  Q
from .models import Room,Topic,Message,User,OtpToken
from .forms import RoomForm,UserForm,NewUserCreationForm
from django.utils import timezone
from datetime import datetime ,timedelta
from django.forms.models import model_to_dict


rooms =Room.objects.all()
generateRandomOtp=lambda :''.join([str(random.randint(0, 9)) for _ in range(6)])

# Create your views here.
def home(req):
    q=req.GET.get('q') if req.GET.get('q') else ''
    # rooms=Room.objects.filter(topic__name__icontains=q)# checks  if the name of the topic contains the query
    # Searching with Q function
    rooms=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) |  Q(description__icontains=q))
    topics=Topic.objects.all()[:5]
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
    topics=Topic.objects.all()
    if req.method=="POST":
        topic_name=req.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=req.user,
            topic=topic,
            name=req.POST.get('name'),
            description=req.POST.get('description'),
        )
        return redirect('home')
    context={'form':form,'topics':topics}
    return render(req,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(req,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if req.user !=room.host:
        return HttpResponse("User action not allowed!!!")
    if req.method=='POST':
        topic_name=req.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=req.POST.get('name')
        room.topic=topic
        room.description=req.POST.get('description')
        room.save()
        return redirect('home')
    context={'form':form,'topics':topics}
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
    return render(req,'base/delete.html',{'obj':msg,'prev_url':req.META['HTTP_REFERER']})

def loginPage(req):
    page='Login'
    if req.user.is_authenticated:
        return redirect('home')
    if  req.method=='POST':
        email=req.POST.get('email')
        password=req.POST.get('password')
        print(email,password)
        try:
            user=User.objects.get(email=email)
            print(user)
            user=authenticate(req,username=user,password=password)
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
    form=NewUserCreationForm()
    if req.method=='POST':
        try:
            form=NewUserCreationForm(req.POST)
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

def userProfile(req,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    topics=Topic.objects.all()
    room_messages=user.message_set.all()
    context={'user':user,'rooms':rooms,'topics':topics,'room_messages':room_messages}
    return render(req,'base/profile.html',context)

@login_required(login_url='login')
def  updateProfile(req):
    user=req.user
    form=NewUserCreationForm(instance=user)
    if req.method=="POST":
        if(req.user.username!=req.POST["username"]):
            user.username=req.POST["username"]
            user.save()
        form=NewUserCreationForm(req.POST,req.FILES,instance=user)
        errors=json.loads(form.errors.as_json())
        # user_name_error=errors.pop("username",None)
        if form.is_valid():
            form.save()
            login(req,user)
            return redirect('user-profile',user.id)
        else:
            for err in errors:
                messages.error(req,err[0].message)
    form.instance.username=req.user.username
    context={'form':form}
    return render(req,'base/edit-user.html',context)

def topicPage(req):
    q=req.GET.get('q') if req.GET.get('q') else ''
    topics=Topic.objects.filter(name__icontains=q)
    context={'topics':topics}
    return render(req,"base/topics.html",context)

def activityPage(req):
    room_messages=Room.objects.all()
    context={'room_messages':room_messages}
    return render(req,"base/activity.html",context)

def verifyEmail(req):
    if req.method=="POST":
        email=req.POST["email"]
        data={
        'expiresAt': timezone.now() + timedelta(minutes=3),  # Use timezone-aware datetime
        'otp': generateRandomOtp()
        }
        print("-----",data)
        otpData=OtpToken.objects.update_or_create(email=email,defaults=data)
        messages.success(req,"An Otp is send to your email")
        return redirect('verify-otp',email)
    context={'step':1}
    return render(req,'base/verify-email.html',context)

def verifyOtp(req,email):
    if req.method=='POST':
        otp=req.POST['otp']
        otpData=OtpToken.objects.get(email=email)
        if(not otpData):
            return redirect('verifyEmail')
        if(otpData.expiresAt<timezone.now()):
            messages.warning(req,"The Otp has expired , get a new OTP !")
            return  redirect('verify-email')
        elif (otpData.otp==otp) :
            messages.success(req,"Account verified successfully !! You can now fill details to sign up ..")
            user=User.objects.create(email=email)
            login(req,user)
            return redirect('update-user')
        else:
            messages.warning(req,"Invalid Otp !!..")
    return render(req,'base/verify-email.html')
