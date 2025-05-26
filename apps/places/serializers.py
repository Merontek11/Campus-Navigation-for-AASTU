from rest_framework import serializers
from .models import Place, Event, GalleryImage, Category
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Place

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'description']

# class PlaceSerializer(serializers.ModelSerializer):
#       class Meta:
#           model = Place
#           fields = '__all__'
class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = ['image']

class EventSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_status(self, obj):
        return obj.status()

class GalleryImageSerializer(serializers.ModelSerializer):
      uploaded_by = serializers.StringRelatedField(read_only=True)

      class Meta:
          model = GalleryImage
          fields = ['id', 'title_en', 'title_am', 'image', 'uploaded_by', 'approved', 'created_at']
          read_only_fields = ['uploaded_by', 'approved', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
      class Meta:
          model = Category
          fields = ['id', 'name']