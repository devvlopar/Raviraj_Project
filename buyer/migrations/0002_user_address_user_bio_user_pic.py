# Generated by Django 4.1.1 on 2022-10-06 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="pic",
            field=models.FileField(default="sad.jpg", upload_to="profile_pic"),
        ),
    ]
