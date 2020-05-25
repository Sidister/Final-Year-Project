from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages, auth
from .models import Profile
import urllib
from .face import pi_face

# Create your views here.
def register(request):
    if request.method=='POST':
        # Get from values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        teacher = request.POST['teacher']

        #Check if password match
        if password==password2:
            #Check Username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    #Looks Good
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    #Login after register
                    #auth.login(request,user)
                    #messages.success(request, 'You are now logged in')
                    #return redirect('index')
                    user.profile.teacher=teacher
                    user.save()
                    messages.success(request, 'You are now registered')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else: 
        return render(request, 'accounts/register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
    if request.user.is_authenticated :
        user = User.objects.get(id=request.user.id)
        return render(request, 'accounts/dashboard_content.html')
    else:
        return redirect('index')
    
def dash_content(request, parameter):
    if parameter=='attendance':
        if request.method == 'POST':
            canvasData = request.POST['canvasData']
            data = canvasData
            response = urllib.request.urlopen(data)
            with open('sawa/static/image.jpg', 'wb') as f:
                f.write(response.file.read())
            names=pi_face.process()

            context = {
                'names' : names,
                'parameter' : parameter
            }
            if len(names)>0:
                messages.success(request, 'Attendance was marked !')
            return render(request, 'accounts/attendance.html', context)

        return render(request, 'accounts/attendance.html')
    else:
        context = {
            'parameter' : parameter
        }
        return render(request, 'accounts/dashboard_content.html', context)