from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from .models import *


# Create your views here.



class LessonForm(forms.Form):
    teachers = User.objects.filter(type="ST")
    time_start = forms.TimeField(
        label="Time of start",
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
    )
    time_end = forms.TimeField(
        label="Time of end",
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
    )
    teacher = forms.ModelChoiceField(queryset=teachers, label="Teacher")
    subject = forms.CharField(max_length=300)

@login_required
def index(request):
    return HttpResponse("Hello, world")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

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
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
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
            
            user = User.objects.create_user(username=username, password=password, group = group, school=school, type=type, first_name=name, last_name=surname, email=email)
        else:
            user = User.objects.create_user(username=username, password=password, school=school, type=type, first_name=name, last_name=surname, email=email)
        
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

@login_required
def plan_view(request):
    if request.method == "POST":
        pass
    else:
        user = request.user
        print(user.type)
        if user.type == "SU":
            user_per = False
        else:
            user_per = True

        return render(request, "classroom/plan.html",{
            "perrmision": user_per,
            "form": LessonForm()
        })


