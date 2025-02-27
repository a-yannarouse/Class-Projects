# File: models.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/20/2025
# Description: This file contains the model for the Profile object.
from django.db import models
from django import forms
from django.urls import reverse

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
    
    def get_absolute_url(self):
        ''' Return a URL to display one instance of this object.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_status_messages(self):
        ''' Return all status messages for this profile.'''
        return StatusMessage.objects.filter(profile=self).order_by('timestamp')
    
class StatusMessage(models.Model):
    ''' Encapsulate the data of a status message.'''

    # Define the data attributes of the StatusMessage object
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        ''' Return a string representation of this model instance.'''
        return f'{self.message}'
    
class CreateProfileForm(forms.ModelForm):
    ''' Form to add a new article to the database.'''

    # Explicitly defining form fields to customize labels and requirements
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email = forms.EmailField(label="Email", required=True)
    image_url = forms.URLField(label="Image URL", required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url']
