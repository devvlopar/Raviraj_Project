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
    

class Blog(models.Model):
    title = models.CharField(max_length = 50)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
    pic = models.FileField(upload_to = 'blogs', default = 'sofo.jpg')

    def __str__(self) -> str:
        return self.title


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    amount = models.FloatField(default = 0.0)

    def __str__(self) -> str:
        return self.user + ' has donated ' + self.blog