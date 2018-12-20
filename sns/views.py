from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
import pyrebase
import datetime
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
        cnt = 0	
        # Create Account 
        user = authe.create_user_with_email_and_password(email, password)
        print (user)
        uid = user['localId']
        data = {'name': username, 'index': cnt, 'id': uid}
        # Set Name & count
        database.child('user').child(uid).child('details').set(data)
        database.child('user').child(uid).child('details').child('follow').set({'length': 0})
        database.child('user').child(uid).child('details').child('follower').set({'length': 0})
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

def my_timeline_api(request):
    items = []
    uid = request.session['ses']
    datas = database.child('user').child(uid).child('timeline').get()
    for data in datas.each():
        items.append(data.val())

    return HttpResponse(json.dumps(items))

def timeline(request):
    try:
        data = database.child('timeline').get().val()
        return render(request,'timeline.html', {'data':data})

    except :
        # message = 'error'
        # return render(request,'timeline.html', {'message':message})
        return redirect('/')

def timeline_post(request):
   content = request.POST.get('content')
   topic = getTopic(content)
   uid = request.session['ses']
   cnt = int(database.child('index').get().val())
   userCnt = int(database.child('user').child(uid).child('details').child('index').get().val())
   # Get now time
   now = datetime.datetime.now()
   date = str(now.year)+'/'+str(now.month)+'/'+str(now.day)+' '+str(now.hour)+':'+str(now.minute)
   print(date)
   # Get username
   username = database.child('user').child(uid).child('details').child('name').get().val()
   # Get id
   id = database.child('user').child(uid).child('details').child('id').get().val()
   # firebase set datas
   datas = {'id': id, 'username': username,'date': date, 'content':content, 'topic':topic}
   database.child('timeline').child(cnt).set(datas)
   database.child('user').child(uid).child('timeline').child(userCnt).set(datas)
   # Add +1 to userCnt
   userCnt +=  1
   database.child('user').child(uid).child('details').child('index').set(userCnt)
   # Add +1 to cnt
   cnt += 1
   database.child('index').set(cnt)
   return redirect(timeline)

def timeline_post_view(request):
    return render(request,'timeline_post.html')

def profile(request):
    try:
        uid = request.session['ses']
        data = database.child('user').child(uid).child('details').get().val()
        print(data)
        return render(request,'profile.html', {'data':data})

    except :
        return redirect('/')

def profile_edit_view(request):
    return render(request,'profile_edit.html')

def profile_edit(request):
    uid = request.session['ses']
    username = request.POST.get('name')
    appeal = request.POST.get('appeal')
    data = {'name': username, 'appeal' : appeal}
    database.child('user').child(uid).child('details').update(data)
    return redirect('profile')

def user_list_api(request):
    items = []
    datas = database.child('user').get()
    for data in datas.each():
        items.append(data.val())

    return HttpResponse(json.dumps(items))    

def user_list(request):
    try:
        data = database.child('user').get().val()
        return render(request,'user_list.html', {'data':data})

    except :
        # message = 'error'
        # return render(request,'timeline.html', {'message':message})
        return redirect('/')

def user_list_view(request):
    return render(request,'user_list.html')

def other_profile(request,methods=['POST']):
    global yid
    yid = request.POST.get('data')
    uid = request.session['ses']
    data = database.child('user').child(yid).child('details').get().val()
    udata = database.child('user').child(uid).child('details').get().val()
    
    followState = database.child('user').child(uid).child('details').child('follow').child(yid).get().val()
    if followState == None:
        database.child('user').child(uid).child('details').child('follow').child(yid).set('false')
        followState = False

    return render(request,'other_profile.html', {'data':data,'udata':udata, 'fstate':followState})
    

def other_timeline_api(request):
    items = []
    datas = database.child('user').child(yid).child('timeline').get()
    for data in datas.each():
        items.append(data.val())

    return HttpResponse(json.dumps(items))

def follow_list(request):
    
    return render(request,'follow_list.html')

def follower_list(request):
    return render(request,'follower_list.html')