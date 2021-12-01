from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import requests

# Create your views here.
def index(request):
    return render(request, "index.html")


def domain(request):
    
    
    if request.user.is_anonymous:
        return redirect("/")
    
    context={}
    if request.method=="POST":
        try:
            domain=request.POST['domain']
            r=requests.get(f"http://localhost:8000/subdomain/{domain}")
            data=r.json()[f"{domain}"]
            context={
                'details': data
            }
        except Exception as e:
            context={
                'details': "Not found"
            }
        
   
    return render(request, "domain.html",context)

def pawned(request):

    if request.user.is_anonymous:
        return redirect("/")

    return render(request, "pawned.html")


def about(request):

    if request.user.is_anonymous:
        return redirect("/")

    return render(request, "about.html")

def loginuser(request):

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,"Successfully logged in")
            return redirect("/domain")
        else:
            messages.warning(request,"Failed to logged in")
            return redirect("/")
            
    return redirect("/")

def signuser(request):

    if request.method=="POST":
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        myuser=User.objects.create_user(username, email,  password1)
        myuser.fname=firstname
        myuser.lname=lastname
        myuser.save()
        messages.success(request,"Successfully sign up new user")
        return redirect("/")

    return redirect("/")

def logoutuser(request):
    logout(request)
    messages.success(request, "Successfully logout")
    return redirect("/")
