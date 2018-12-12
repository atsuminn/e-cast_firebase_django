from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
import pyrebase
from firebase import firebase
from django.contrib import auth
import json
# Create your views here.

config = {
    "apiKey": "AIzaSyAKN-uHYzzp2Gdv7kNc3U8qXT-OB7GkVY0",
    "authDomain": "e-east.firebaseapp.com",
    "databaseURL": "https://e-east.firebaseio.com",
    "projectId": "e-east",
    "storageBucket": "e-east.appspot.com"
    }

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


def index(request):
    try:
        uid = request.session['ses']
        if uid is not None:
            return render(request, 'home.html')

    except :
        return render(request,'index.html')

def signin(request):
    if request.method == 'POST':
        global email
        email = request.POST.get('email')
        email = str(email).rstrip(' \t\r\n\0') #new line added here --------
        password = request.POST.get('password')
        try:
            user = authe.sign_in_with_email_and_password(email, password)
            print(user)
        except :
            message = "error"
            return render(request,'signin.html', {'message':message})
        uid = user['localId']
        request.session['ses'] = uid
        aiu = request.session['ses']
        message = 'success' 
        return render(request,'home.html', {'message':message,'aiu':aiu})

    else:
        return render(request,'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')	
        # Create Account 
        user = authe.create_user_with_email_and_password(email, password)
        print (user)
        uid = user['localId']
        data = {'name': username}
        # Set Name
        database.child(uid).child("details").set(data)
        message = 'success'
        return render(request,'signin.html', {'message':message})
    else:
	    return render(request,'signup.html')

def signout(request):
    request.session.flush()
    return render(request,'index.html')	

def timeline_api(request):
    items = []
    datas = database.child('timeline').get()
    for data in datas.each():
        items.append(data.val())

    return HttpResponse(json.dumps(items))
    # return render(request,'timeline.html')
def timeline(request):
    return render(request, 'timeline.html')

def profile(request):
    try:
        uid = request.session['ses']
        data = database.child(uid).child("details").get().val()
        return render(request,'profile.html', {'data':data})

    except :
        return redirect('/')

def profile_edit_view(request):
    return render(request,'profile_edit.html')

def profile_edit(request):
    uid = request.session['ses']
    print(uid)
    username = request.POST.get('name')
    appeal = request.POST.get('appeal')
    data = {'name': username, 'appeal' : appeal}
    database.child(uid).child("details").update(data)

    return redirect('profile')


    
        