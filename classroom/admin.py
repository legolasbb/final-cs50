from django.contrib import admin
from .models import User, School, Class, Lesson, Homework, homework_submission, Grade

# Register your models here.

admin.site.register(User)
admin.site.register(School)
admin.site.register(Class)
admin.site.register(Lesson)
admin.site.register(Homework)
admin.site.register(homework_submission)
admin.site.register(Grade)