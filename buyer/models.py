from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    pic = models.FileField(upload_to='profile_pic', default='sad.jpg')
    address = models.TextField(null = True, blank = True)
    bio = models.TextField(null = True, blank= True)

    def __str__(self):
        return self.first_name
    