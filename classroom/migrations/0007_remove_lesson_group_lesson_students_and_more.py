# Generated by Django 4.2.16 on 2024-11-21 08:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0006_alter_lesson_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='group',
        ),
        migrations.AddField(
            model_name='lesson',
            name='students',
            field=models.ManyToManyField(related_name='student_lessons', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.CharField(choices=[('MA', 'Math'), ('IT', 'Information technology'), ('EN', 'English'), ('BL', 'Biology'), ('CH', 'Chemistry'), ('PH', 'Physics'), ('GE', 'Geography'), ('HI', 'History')], max_length=300),
        ),
    ]