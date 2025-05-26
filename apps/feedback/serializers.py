from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
import re
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'comment', 'rating', 'route', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise ValidationError("Rating must be between 1 and 5")
        return value

    def validate_comment(self, value):
        if len(value.strip()) < 5:
            raise ValidationError("Comment must be at least 5 characters long")
        return value

    def validate_route(self, value):
        if value and value.user != self.context['request'].user:
            raise ValidationError("You can only provide feedback for your own routes")
        return value