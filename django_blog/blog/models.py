from django.db import models
from django.db.models import DateField
from django.contrib.auth.models import User

class Post(models.Model): # Defined a model named Post
    title = models.CharField(max_length = 200) # Title of the blog post
    content = models.TextField() # Use TextField for larger text content
    published_date = models,DateField(auto_now_add=True) # Automatically set the field to now when the object is first created
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts') # Link to the User model

    def __str__(self): # Define the string representation of the Post model
        return self.title # Return the title of the post as its string representation