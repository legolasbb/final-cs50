from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

USER_TYPE_CHOICES = {
    "ST": "STUFF",
    "SU": "STUDENT", 
}

DAY_CHOICES = {
    "MON": "MONDAY",
    "TUE": "TUESDAY",
    "WED": "WEDNESDAY",
    "THU": "THURSDAY",
    "FRI": "FRIDAY",
}

class School(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254    )

class Class(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    

class User(AbstractUser):
    type = models.CharField(max_length=3, choices=USER_TYPE_CHOICES)
    group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="class_studensts")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="school_students")

class Lesson(models.Model):
    subject = models.CharField(max_length=300)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    time_start = models.TimeField()
    time_end = models.TimeField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons")
    students = models.ManyToManyField(User, on_delete=models.CASCADE, related_name="lessons")

class Homework(models.Model):
    subject = models.CharField(max_length=300)
    content = models.CharField()
    deadline = models.DateField()
    group = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="homeworks")

class homework_submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    content = models.CharField(max_length=10000)

    