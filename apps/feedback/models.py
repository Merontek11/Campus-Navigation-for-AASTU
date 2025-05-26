from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    comment = models.TextField(max_length=1000)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    # route = models.ForeignKey(FavoriteRoute, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback by {self.user.username} ({self.rating}/5)"