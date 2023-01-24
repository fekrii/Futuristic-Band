from django.contrib import admin
from .models import ChildProfile, ChildWallet, ChildDaysOff


admin.site.register(ChildProfile)
admin.site.register(ChildWallet)
admin.site.register(ChildDaysOff)

