from rest_framework import serializers
from .models import NavigationInstruction

class NavigationInstructionSerializer(serializers.ModelSerializer):
      class Meta:
          model = NavigationInstruction
          fields = '__all__'