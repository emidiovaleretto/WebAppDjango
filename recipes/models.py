from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Recipe(models.Model):

    objects = None
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    ingredients = models.TextField()
    directions = models.TextField()
    time_to_cook = models.IntegerField()
    servings = models.TextField(max_length=100)
    category = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now, blank=True)
    image = models.ImageField(upload_to='images/%d/%m/%Y/', blank=True)
    published = models.BooleanField(default=True)
    favorite = models.ManyToManyField(User, related_name='favorite', blank=True)

    def __str__(self):
        return self.name
