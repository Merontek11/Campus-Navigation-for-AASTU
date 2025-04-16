from rest_framework import serializers
from .models import Place
from .models import Event
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
