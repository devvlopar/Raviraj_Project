# Generated by Django 4.1.1 on 2022-10-13 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0002_user_address_user_bio_user_pic"),
    ]

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("content", models.TextField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("pic", models.FileField(default="sofo.jpg", upload_to="blogs")),
                (
                    "writer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="buyer.user"
                    ),
                ),
            ],
        ),
    ]
