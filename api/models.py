from django.db import models

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('dorm', 'Dorm'),
        ('library', 'Library'),
        ('lab', 'Lab'),
        ('classroom', 'Classroom'),
        ('office', 'Office'),
        ('cafe', 'Cafe'),
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
from .models import Place  # assuming Event and Place are in the same app

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
    location = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='events')  # 🔗 Linked to Place
    date = models.DateTimeField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title

