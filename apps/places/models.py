from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True, default="General")
#     description = models.TextField(blank=True, default="No description")

#     def __str__(self):
#         return self.name


class Place(models.Model):
    CATEGORY_CHOICES = [
        ('dorm', 'Dorm'),
        ('library', 'Library'),
        ('lab', 'Lab'),
        ('classroom', 'Classroom'),
        ('office', 'Office'),
        ('cafe', 'Cafe'),
        ('fun and games', ' Fun and Games'),
          ('shop', 'Shop'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='place_images/', null=True, blank=True)
    def __str__(self):
        return self.name

# class Event(models.Model):
#       CATEGORY_CHOICES = [
#           ('seminar', 'Seminar'),
#           ('sports', 'Sports'),
#           ('music', 'Music'),
#           ('meeting', 'Meeting'),
#           ('other', 'Other'),
#       ]

#       title = models.CharField(max_length=255)
#       description = models.TextField()
#       location = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='events')
#       date = models.DateTimeField()
#       category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

#       def __str__(self):
#           return self.title

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
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)  

    def __str__(self):
        return self.title

    def status(self):
        now = timezone.now()
        if self.start_date <= now <= self.end_date:
            return "ongoing"
        elif self.start_date > now:
            return "upcoming"
        else:
            return "completed"

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
      name = models.CharField(max_length=100)

      def __str__(self):
          return self.name