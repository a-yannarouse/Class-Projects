# File: admin.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/11/2025
# Description: This file contains the admin settings for the Profile model.
from django.contrib import admin
from .models import Profile, StatusMessage

# Register your models here.
admin.site.register(Profile)
admin.site.register(StatusMessage)