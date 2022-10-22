# Generated by Django 4.1.2 on 2022-10-22 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('TCH', 'استاد'), ('STU', 'دانشجو')], max_length=30, null=True),
        ),
    ]
