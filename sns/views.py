from django.http import HttpResponse
from django.shortcuts import render
import pyrebase
from firebase import firebase
from django.contrib import auth
# Create your views here.

name = " "
email = " " 
config = {
    
    }

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def index(request):
	return render(request,'index.html')

def signin(request):
    if request.method == 'POST':
        global email
        email = request.POST.get('email')
        email = str(email).rstrip(' \t\r\n\0') #new line added here --------
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            message = 'success'
            return render(request,'home.html', {'message':message})
        except :
            message = "error"
            return render(request,'signin.html', {'message':message})
    else:
        return render(request,'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('name_field')
        password = request.POST.get('password')
        email = request.POST.get('email')	

        user = authe.create_user_with_email_and_password(email, password)
        # print (user)
        # uid = user['localId']
        # data = {"name": username,"status":"1"}
        # database.child("e-cast").child(uid).child("details").set(data)
        message = 'success'
        return render(request,'signin.html', {'message':message})
    else:
	    return render(request,'signup.html')

def signout(request):
    return render(request,'index.html')	

def timeline(request):
    return render(request,'timeline.html')