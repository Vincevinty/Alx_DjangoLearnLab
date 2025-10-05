from django.db import models
from django.db.models import DateField
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    published_date = models,DateField(auto_now_add=True)
    author = models.Foreignkey(User, on_delete = models.CASCADE, related_name = 'posts')


