from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *


# Create your views here.


def index(request):
    return HttpResponse("Hello, world")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "classroom/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "classroom/login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        type = request.POST['type']
        school_code = request.POST['school']

        try:
            school = School.objects.get(name=school_code)
        except School.DoesNotExist:
            return render(request, "classroom/register.html", {
                "message": "School does not exist"
            })
    # Handle the case where the school is not found
        print(school)
        if password != confirmation:
            return render(request, "classroom/register.html", {
                "message": "Passwords must match."
            })

        if type == "SU":
            group_code = request.POST['class']
            try:
                group = Class.objects.get(name=group_code)
            except Class.DoesNotExist:
                return render(request, "classroom/register.html", {
                    "message": "Class does not exist"
                })
            
            user = User.objects.create_user(username=username, password=password, group = group, school=school)
        else:
            user = User.objects.create_user(username=username, password=password, school=school)
        
        try:
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "classroom/register.html")