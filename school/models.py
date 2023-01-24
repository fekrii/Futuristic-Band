from django.db import models
from _auth.models import CustomUser


class School(models.Model):
    user = models.OneToOneField(CustomUser, related_name="SchoolProfile", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name