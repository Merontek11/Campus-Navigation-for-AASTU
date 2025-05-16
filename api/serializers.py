from rest_framework import serializers
from .models import Place
from .models import Event
from .models import GalleryImage
from .models import Category 
from .models import NavigationInstruction
from django.contrib.auth.models import User

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
class EventSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)  # to show readable name

    class Meta:
        model = Event
        fields = '__all__'


class GalleryImageSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GalleryImage
        fields = ['id', 'title', 'image', 'uploaded_by', 'is_approved', 'created_at']
        read_only_fields = ['uploaded_by', 'is_approved', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_en', 'name_am']
class NavigationInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationInstruction
        fields = '__all__'