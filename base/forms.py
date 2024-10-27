from django.forms import ModelForm
from .models import Room,User
from django.contrib.auth.forms import UserCreationForm

# from django.contrib.auth.models import User

class NewUserCreationForm(UserCreationForm):
    class  Meta:
        model=User
        fields=['name','password1','password2','avatar','bio']

class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__'
        exclude=['host','participants']
        
class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['name','username','email','avatar','bio']