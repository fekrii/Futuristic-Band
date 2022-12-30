from django.db import models
from _auth.models import CustomUser

class ParentProfile(models.Model):

    parent_type = (

        ("Father", "father"),

        ("Mother", "mother")

    )

    user = models.OneToOneField(CustomUser, related_name="ParentProfile", on_delete=models.CASCADE)
    firstName = models.CharField(max_length=255, blank=True, null=True)
    lastName = models.CharField(max_length=255, blank=True, null=True)
    parent_type = models.CharField(max_length=10, choices=parent_type ,blank=True, null=True)
    birthDate = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100 , blank=True, null=True)
    jobTitle = models.CharField(max_length=50 , blank=True, null=True)
    nationality = models.CharField(max_length=50 , blank=True, null=True)

    # is already added in the customuser model,should be removed from here
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.firstName