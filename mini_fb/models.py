# File: models.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/20/2025
# Description: This file contains the model for the Profile object.
from django.db import models

# Create your models here.
class Profile(models.Model):
    ''' Encapsulate the data of a user profile.'''
    
    # Define the data attributes of the Profile object
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.EmailField()
    image_url = models.URLField(blank=True)
    
    def __str__(self):
        ''' Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        ''' Return all status messages for this profile.'''
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
class StatusMessage(models.Model):
    ''' Encapsulate the data of a status message.'''

    # Define the data attributes of the StatusMessage object
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        ''' Return a string representation of this model instance.'''
        return f'{self.message}'