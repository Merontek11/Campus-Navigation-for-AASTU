from django.db import models

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('dorm', 'Dorm'),
        ('library', 'Library'),
        ('lab', 'Lab'),
        ('classroom', 'Classroom'),
        ('office', 'Office'),
        ('cafe', 'Cafe'),
        ('fun', 'Fun'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='place_images/', null=True, blank=True)
    def __str__(self):
        return self.name
from django.db import models
from .models import Place  

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('seminar', 'Seminar'),
        ('sports', 'Sports'),
        ('music', 'Music'),
        ('meeting', 'Meeting'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='events') 
    date = models.DateTimeField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title

from django.contrib.auth.models import User

class GalleryImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery_images')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User

class GalleryImage(models.Model):
    title_en = models.CharField(max_length=100)
    title_am = models.CharField(max_length=100, blank=True)
    description_en = models.TextField(blank=True)
    description_am = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_en


class Category(models.Model):
    name_en = models.CharField(max_length=100)
    name_am = models.CharField(max_length=100)

    def __str__(self):
        return self.name_en
class NavigationInstruction(models.Model):
    instruction_en = models.CharField(max_length=255)
    instruction_am = models.CharField(max_length=255, blank=True, null=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="navigation_instructions")
    step_order = models.PositiveIntegerField(help_text="Order of this instruction in a route")

    def __str__(self):
        return f"{self.instruction_en} (Step {self.step_order})"
