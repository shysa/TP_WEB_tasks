# Generated by Django 3.0.4 on 2020-04-07 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask_bolgova', '0010_auto_20200407_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar.png', upload_to='uploads/'),
        ),
    ]
