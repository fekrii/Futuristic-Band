from django.db import models
from _auth.models import CustomUser
from school.models import School
from parent.models import ParentProfile

class ChildProfile(models.Model):
    
    child_at_options = (

        ("At Bus", "At Bus"),

        ("At School", "At School"),
        
        ("At ClassRoom", "At ClassRoom")
        

    )
    parent = models.ForeignKey(ParentProfile, related_name='ChildParent', on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser, related_name="ChildProfile", on_delete=models.CASCADE)
    firstName = models.CharField(max_length=255, blank=True, null=True)
    lastName = models.CharField(max_length=255, blank=True, null=True)
    birthDate = models.DateField(blank=True, null=True)
    school = models.ForeignKey(School, related_name="ChildSchool", on_delete=models.CASCADE)
    child_at = models.CharField(max_length=255, choices=child_at_options ,blank=True, null=True)
    banned_food = models.JSONField(default=[])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.firstName)


class ChildWallet(models.Model):
    child = models.OneToOneField(ChildProfile, related_name="ChildWallet", on_delete=models.CASCADE)
    max_amount = models.IntegerField(default=500)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'wallet for : {self.child.firstName}'


class ChildDaysOff(models.Model):
    child = models.ForeignKey(ChildProfile, related_name="ChildDayOff", on_delete=models.CASCADE)
    day = models.DateField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'day off for : {self.child.firstName}'
