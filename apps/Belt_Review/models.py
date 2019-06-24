from django.db import models

# Create your models here.

class User(models.Model):
    full_name = models.CharField(max_length = 60)
    alias = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Book(models.Model):
    title = models.CharField(max_length = 60)
    description = models.CharField(max_length = 60)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Author(models.Model):
    full_name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name="authors")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    review = models.CharField(max_length=255)
    rating = models.IntegerField()
    creator = models.CharField(max_length=60)
    creator_id = models.IntegerField()
    books = models.ManyToManyField(Book, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)