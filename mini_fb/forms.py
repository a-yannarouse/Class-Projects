# File: forms.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/25/2025
# Description: This file contains the model for the Profile form object.
from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    ''' Form to add a new article to the database.'''
    
    class Meta:
        ''' Define the model and fields of the form.'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    ''' Form to add a new status message to the database.'''
    
    class Meta:
        ''' Define the model and fields of the form.'''
        model = StatusMessage
        fields = ['message']   

class UpdateProfileForm(forms.ModelForm):
    ''' A form to handle an update to a Profile.'''
    
    class Meta:
        model = Profile
        fields = ['city', 'email', 'image_url']