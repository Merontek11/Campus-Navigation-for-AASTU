from django.contrib import admin
from .models import Place, Event, GalleryImage, Category

admin.site.register(Place)
admin.site.register(Event)
admin.site.register(GalleryImage)
admin.site.register(Category)