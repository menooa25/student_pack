# Generated by Django 4.1.2 on 2022-12-13 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0007_lesson_class_number'),
        ('teacher_note', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lessons.lesson'),
        ),
    ]