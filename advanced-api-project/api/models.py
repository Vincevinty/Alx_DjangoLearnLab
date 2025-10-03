from django.db import models

class Author(models.Model): # Defines the Author model
    name = models.CharField(max_length = 200) # Stores the author's name

    def __str__(self): # String representation of the Author model
        return self.name # Returns the author's name
    
class Book(models.Model): # Defines the Book model
    title = models.CharField(max_length = 200) # Stores the book's title
    publication_year = models.IntegerField() # Stores the publication year of the book
    author = models.ForeignKey(Author, on_delete = models.CASCADE) # Links to the Author model

    def __str__(self): # String representation of the Book model
        return self.title # Returns the book's title
