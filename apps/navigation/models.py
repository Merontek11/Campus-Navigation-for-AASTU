from django.db import models
from apps.places.models import Place

class NavigationInstruction(models.Model):
      instruction_en = models.CharField(max_length=255)
      instruction_am = models.CharField(max_length=255, blank=True, null=True)
      place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="navigation_instructions")
      step_order = models.PositiveIntegerField(help_text="Order of this instruction in a route")

      def __str__(self):
          return f"{self.instruction_en} (Step {self.step_order})"