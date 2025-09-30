from django.db import models

class Author(models.Model):
    name = models.CharField(max_length = 200) # Stores author's name

    def __str__(self): 
        return self.name # Returns the author's name when the object is printed or displayed in the admin panel

# Each book is linked to one Author using a ForeignKey, creating a one-to-many relationship.    
class Book(models.Model): 
    title = models.CharField(max_length = 200) # Stores book title
    publication_year = models.IntegerField() # Stores publication year
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE) # Links to Author model

    def __str__(self): 
        return self.title  # Returns the book's title when the object is printed or displayed in the admin panel
