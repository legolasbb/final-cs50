# Generated by Django 4.2.16 on 2024-11-20 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0004_remove_lesson_students_lesson_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_lessons', to='classroom.class'),
        ),
    ]
