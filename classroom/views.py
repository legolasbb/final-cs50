from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from datetime import *
from .models import *


# Create your views here.
DAY_CHOICES = [
    ("MON", "MONDAY"),
    ("TUE", "TUESDAY"),
    ("WED", "WEDNESDAY"),
    ("THU", "THURSDAY"),
    ("FRI", "FRIDAY"),
]

SUBJECT_CHOICES = [
    ("MA", "Math"),
    ("IT", "Information technology"),
    ("EN", "English"),
    ("BL","Biology"),
    ("CH","Chemistry"),
    ("PH","Physics"),
    ("GE", "Geography"),
    ("HI", "History"),
]



@login_required
def index(request):
    return render(request, "classroom/index.html")

@login_required
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

#check for time confict
def check_time(time_add_start, time_add_end, time_2_start, time_2_end):
    if time_2_start < datetime.strptime(time_add_start, "%H:%M").time() and time_2_end < datetime.strptime(time_add_start, "%H:%M").time():
        return True
    elif datetime.strptime(time_add_end, "%H:%M").time() <=time_2_start:
        return True
    else: 
        return False

@login_required
def plan_view(request):
    user = request.user
    if request.method == "POST":
        #data needed for validity check
        teacher_id = request.POST['teacher']
        group_id = request.POST['class']
        day = request.POST['day']
        time_start = request.POST['start_time']
        time_end = request.POST['end_time']
        teacher = User.objects.get(pk=teacher_id)
        group = Class.objects.get(pk=group_id)
        #checks for confilct in plan
        class_lessons = group.class_lessons.all().filter(day=day)
        teacher_lessons = teacher.teacher_lessons.filter(day=day)
        #confilct in class
        for lesson in class_lessons:
            if check_time(time_start, time_end, lesson.time_start, lesson.time_end)==False:
                return render(request, "classroom/plan.html", {
                    "message": "Time conflict"
                })
        
        #conflict in lesson
        for lesson in teacher_lessons:
            if check_time(time_start, time_end, lesson.time_start, lesson.time_end)==False:
                return render(request, "classroom/plan.html", {
                    "message": "Time conflict"
                })
        
        #check if time is valid
        if time_start>time_end:
            return render(request, "classroom/plan.html", {
                "message": "Invalid time"
            })
        
        
        #rest of data
        subject = request.POST['subject']
        #create new lesson
        lesson = Lesson.objects.create(subject=subject, day=day, time_start=time_start, time_end=time_end, teacher=teacher, group=group)
        lesson.save()
        return render(request, "classroom/plan.html", {
            "message": "Lesson created"
        })
    else:
        #display form only if user is staff and get all lessons
        if user.type == "SU":
            #student
            user_per = False
            group = user.group
            lessons = group.class_lessons.all()
        else:
            #teacher
            user_per = True
            lessons = user.teacher_lessons.all()
        
        school = user.school
        grups = school.classes.all()
        teachers = User.objects.filter(type="ST", school=school)
        return render(request, "classroom/plan.html",{
            "subjects": SUBJECT_CHOICES,
            "perrmision": user_per,
            "teachers": teachers,
            "days": DAY_CHOICES,
            "classes": grups,
            "lessons": lessons
        })

@login_required
def homework_teacher_view(request):
    #add deadline validation 

    user= request.user
    if request.method == "POST":
        subject = request.POST['subject']
        content = request.POST['content']
        deadline = request.POST['deadline']
        group_id = request.POST['group']
        group = Class.objects.get(pk=group_id)
        homework = Homework.objects.create(subject=subject, content=content, deadline=deadline, group=group, teacher=user)
        homework.save()
        return render(request, "classroom/teacher_homework.html", {
            "message": "Homework created"
        })
    else:
        given_homeworks = user.given_homeworks.all()
        school = user.school
        grups = school.classes.all()
        return render(request, "classroom/teacher_homework.html", {
            "homeworks": given_homeworks,
            "classes": grups,
            "subjects": SUBJECT_CHOICES,
        })
        

