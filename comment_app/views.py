from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'login.html')


def register(request):
    if request.method =='POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  
            print(pw_hash)
            request.session['username'] = fname
            
           
            User.objects.create(first_name=fname, last_name=lname,email=email, password=pw_hash)
    return redirect("/")

def login(request):
    if request.method =='POST':
        errors2 = User.objects.login_validator(request.POST)
        if len(errors2) > 0:
            for key, value in errors2.items():
                messages.error(request, value)
            return redirect('/')

        users = User.objects.filter(email=request.POST['email2'])
        if users:
            logged_user = users[0]
            if bcrypt.checkpw(request.POST['password2'].encode(), logged_user.password.encode()):
                request.session['username'] = logged_user.first_name
                request.session['status']="logged in"
                request.session['userid'] = logged_user.id
                return redirect('/wall')
            print("""Wrong password""")
        return redirect("/")
def wall(request):
    context = {
        "all_messages":Message.objects.all(),
        'comments':Comment.objects.all(),
        'first_name':request.session['username']
    }
    return render(request,'wall.html',context)

def post_mes(request):
    if request.method =='POST':
        Message.objects.create(
            message_text = request.POST['message-user'],
            user = User.objects.get(id = request.session['userid'] )
        )
        
    return redirect('/wall')  
def post_comm(request):
      if request.method =='POST':
          
          Comment.objects.create(
              comment_text = request.POST['comment-user'],
              user = User.objects.get(id = request.session['userid'] ),
              message =  Message.objects.get(id =request.session['userid'])
          )
          
      return redirect('/wall')    
def logout(request):
    del request.session['username']
    del request.session['status']
    request.session['userid']
   
    return redirect('/')   

            




       


