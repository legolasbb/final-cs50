# Generated by Django 4.2.16 on 2025-05-22 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0009_homework_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='subject',
            field=models.CharField(choices=[('MA', 'Math'), ('IT', 'Information technology'), ('EN', 'English'), ('BL', 'Biology'), ('CH', 'Chemistry'), ('PH', 'Physics'), ('GE', 'Geography'), ('HI', 'History')], max_length=300),
        ),
    ]
