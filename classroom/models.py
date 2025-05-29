from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

USER_TYPE_CHOICES = [
    ("ST", "STUFF"),
    ("SU", "STUDENT"), 
]

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

class School(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

class Class(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES, null=True)
    group = models.ForeignKey(Class, on_delete=models.CASCADE, null=True ,related_name="class_students")
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True ,related_name="school_students")
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Lesson(models.Model):
    subject = models.CharField(max_length=300, choices=SUBJECT_CHOICES)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    time_start = models.TimeField()
    time_end = models.TimeField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_lessons")
    group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="class_lessons")

class Homework(models.Model):
    subject = models.CharField(max_length=300, choices=SUBJECT_CHOICES)
    content = models.CharField(max_length=10000)
    deadline = models.DateField()
    group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="homeworks")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_homeworks")

class homework_submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name="students_submissions")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_submissions")
    content = models.CharField(max_length=10000)    