# File: admin.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/11/2025
# Description: This file contains the admin settings for the Profile model.
from django.contrib import admin #type: ignore
from .models import Profile, StatusMessage, Image, StatusImage, Friend

# Register your models here.
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)
admin.site.register(Friend)