from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from datetime import *
from .models import *
from django.contrib import messages


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
    user=request.user
    permission=True
    grades = list()
    if user.type == "SU":
        #student
        group = user.group
        homeworks = group.homeworks.filter(deadline__gte=date.today()).order_by('deadline')
        #get submissions in order to get grades
        submissions = user.my_submissions.all()
       
        i =0
        for submission in submissions:
            if i>=3:
                break
            if submission.grade.first():
                i+=1
                grades.append(submission.grade.first())
    else:
        permission=False
        #teacher
        homeworks = user.given_homeworks.all().filter(deadline__gte=date.today()).order_by('deadline')[:3]
    return render(request, "classroom/index.html", {
        "homeworks": homeworks,
        "grades": grades,
        "permission": permission
    })

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
                messages.error(request, "Time conflict")
                return redirect('plan')
        
        #conflict in lesson
        for lesson in teacher_lessons:
            if check_time(time_start, time_end, lesson.time_start, lesson.time_end)==False:
                messages.error(request, "Time conflict")
                return redirect('plan')
        
        #check if time is valid
        if time_start>time_end:
            messages.error(request, "Time conflict")
            return redirect('plan')
        
        
        #rest of data
        subject = request.POST['subject']
        #create new lesson
        lesson = Lesson.objects.create(subject=subject, day=day, time_start=time_start, time_end=time_end, teacher=teacher, group=group)
        lesson.save()
        messages.success(request, "Lesson created")
        return redirect('plan')
        '''return render(request, "classroom/plan.html", {
            "message": "Lesson created"
        })'''
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
def homework_view(request):
    #add deadline validation 
    user= request.user

    if user.type=="SU":
        #student
        if request.method=="POST":
            subject = request.POST['subject']
        else:
            #get and display all homeworks
            group=user.group
            homeworks = group.homeworks.filter(deadline__gte=date.today()).order_by('deadline')
            return render(request, "classroom/homework.html", {
                "homeworks": homeworks,
                "perrmision": False
            })
    else:
        #teacher
        if request.method == "POST":
            #get all details and create new homework
            subject = request.POST['subject']
            content = request.POST['content']
            deadline = request.POST['deadline']
            group_id = request.POST['group']
            group = Class.objects.get(pk=group_id)
            homework = Homework.objects.create(subject=subject, content=content, deadline=deadline, group=group, teacher=user)
            homework.save()
            messages.success(request, "Homework created")
            return redirect('homework')
        else:
            #get homeworks by ordered by deadline and request the,
            given_homeworks = user.given_homeworks.order_by('-deadline')
            school = user.school
            grups = school.classes.all()
            return render(request, "classroom/homework.html", {
                "homeworks": given_homeworks,
                "classes": grups,
                "subjects": SUBJECT_CHOICES,
                "perrmision": True
            })
        
@login_required
def homework_submission_view(request, homework_id):
    user = request.user
    homework = Homework.objects.get(pk=homework_id)

    if user.type == "SU":
        #student
        if request.method == "POST":
            #get post and submit homework submission
            content = request.POST['content']
            submission = homework_submission.objects.create(homework=homework, student=user, content=content)
            submission.save()
            messages.success(request, "Submited succesfully")
            return redirect('homework')
        else:
            #display submission form
            homework = Homework.objects.get(pk=homework_id)
            return render(request, "classroom/submission.html", {
                "homework": homework
            })
    else:
        #teacher
        if request.method == "POST":
            submissions = homework.students_submissions.all()
            if request.POST['type'] == 'grade':
                grade  = request.POST['grade']
                feedback = request.POST['feedback']
                submission_id=request.POST['submission.id']
                submission=homework_submission.objects.get(pk=submission_id)
                grade = Grade.objects.create(grade=grade, feedback=feedback, submission=submission, teacher=user)
                grade.save()
            else:
                grade  = request.POST['grade']
                feedback = request.POST['feedback']
                grade_id=request.POST['submission.id']
                grade_edit = Grade.objects.get(pk=grade_id)
                grade_edit.grade=grade
                grade_edit.feedback=feedback
                grade_edit.save()
            return render(request, "classroom/submissions.html",{
                "submissions": submissions,
                "homework": homework
            })
        else:
            submissions = homework.students_submissions.all()
            return render(request, "classroom/submissions.html",{
                "submissions": submissions,
                "homework": homework
            })
        
def grade_view(request):
    user = request.user
    if user.type == "SU":
        submissions = user.my_submissions.all()
        averages = []
        #calculate average for every subject
        for subject in SUBJECT_CHOICES:
            subject_name = subject[1]
            sum = 0
            amount = 0
            for submission in submissions:
                if subject_name == submission.homework.get_subject_display():
                    for grade in submission.grade.all():
                        sum+=grade.grade
                        amount+=1
            if amount == 0:
                averages.append((subject_name, 0))
            else:
                averages.append((subject_name, round(sum / amount, 2)))
        return render(request, "classroom/su_grade.html",{
            "submissions": submissions,
            "subjects": averages 
        })
    else:
        #getting all grades given to the students
        grades = user.students_grades.all()
        students = set()
        subjects = set()
        for grade in grades:
            students.add(grade.submission.student)
            subjects.add(grade.submission.homework.get_subject_display())
        students_list=list(students)
        subjects_list = list(subjects)
        return render(request, "classroom/st_grade.html",{
            "grades": grades,
            "students":students_list,
            "subjects": subjects_list
        })
