from django.contrib import admin
from .models import User, School, Class, Lesson

# Register your models here.

admin.site.register(User)
admin.site.register(School)
admin.site.register(Class)
admin.site.register(Lesson)