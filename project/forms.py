# File: forms.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 04/18/2025
# Description: This file contains the forms for the project app. 

from django import forms
from .models import *

class SubmissionForm(forms.ModelForm):
    """Form for creating a new submission."""
    class Meta:
        model = Submission
        fields = ['name', 'profile_type', 'nationality', 'bio', 'location', 'website_or_channel', 'reason_for_submission', 'photo', 'tags']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo', 'interests']
        widgets = {
            'interests': forms.CheckboxSelectMultiple,
            'tags': forms.CheckboxSelectMultiple()
        }
        labels = {
            'photo': 'Profile Photo',
            'interests': 'Interests',
            'tags': 'Tags'
        }
        help_texts = {
            'photo': 'Upload a profile photo (optional).',
            'interests': 'Select your interests.',
            'tags': 'Select relevant tags.'
        }
        error_messages = {
            'photo': {
                'invalid': 'Invalid file type. Please upload a valid image.',
            },
            'interests': {
                'required': 'Please select at least one interest.',
            },
            'tags': {
                'required': 'Please select at least one tag.',
            }
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name',
            'profile_type',
            'nationality',
            'bio',
            'location',
            'website_or_channel',
            'photo',
            'tags',
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

class WorkSubmissionForm(forms.ModelForm):
    class Meta:
        model = WorkSubmission
        fields = ['creator', 'title', 'platform', 'description', 'type', 'image', 'link']