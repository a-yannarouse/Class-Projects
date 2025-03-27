# File: models.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/20/2025
# Description: This file contains the model for the Profile object.
from django.db import models # type: ignore
from django import forms # type: ignore
from django.urls import reverse # type: ignore
from django.contrib.auth.models import User # type: ignore

# Create your models here.
class Profile(models.Model):
    ''' Encapsulate the data of a user profile.'''
    
    # Define the data attributes of the Profile object
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.EmailField()
    image_url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        ''' Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        ''' Return a URL to display one instance of this object.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_status_messages(self):
        ''' Return all status messages for this profile.'''
        return StatusMessage.objects.filter(profile=self).order_by('timestamp')
    
    def get_friends(self):
        ''' Return a list of friends for this profile.'''
        friends = []

        for friend in Friend.objects.filter(profile1=self):
            friends.append(friend.profile2)

        for friend in Friend.objects.filter(profile2=self):
            friends.append(friend.profile1)

        return friends
    
    def add_friend(self, other):
        ''' Add a friend relationship between this profile and another.'''
        Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        ''' Return a list of friend suggestions for this profile.'''
        
        # Get all profiles except the current one
        all_profiles = Profile.objects.exclude(pk=self.pk)
        
        # Get current friends
        current_friends = self.get_friends()
        
        # Exclude current friends from the suggestions
        suggestions = all_profiles.exclude(pk__in=[friend.pk for friend in current_friends])
        
        return suggestions
    
    def get_news_feed(self):
        ''' Return a list of status messages from friends.'''
        
        # Get friends
        friends = self.get_friends()
        
        # Get status messages from friends
        news_feed = StatusMessage.objects.filter(profile__in=friends).order_by('-timestamp')
        
        return news_feed
    
class StatusMessage(models.Model):
    ''' Encapsulate the data of a status message.'''

    # Define the data attributes of the StatusMessage object
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        ''' Return a string representation of this model instance.'''
        return f'{self.message}'
    
    def get_images(self):
        '''
        Returns a QuerySet of Image objects associated with this status message
        by following the StatusImage relationship.
        '''
        return Image.objects.filter(statusimage__status_message=self)
    
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

class Image(models.Model):
    ''' Encapsulate the data of an image.'''

    # Define the data attributes of the Image object
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(upload_to='images/')
    caption = models.TextField(blank=True, null=True)

    def __str__(self):
        ''' Return a string representation of this model instance.'''
        return f'Image uploaded by {self.profile} on {self.timestamp}'

class StatusImage(models.Model):
    ''' Encapsulate the data of a status image.'''

    # Define the data attributes of the StatusImage object
    image_file = models.ForeignKey(Image, on_delete=models.CASCADE)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

    def __str__(self):
        ''' Return a string representation of this model instance.'''
        return f'Image {self.image_file.id} associated with StatusMessage {self.status_message.id}'
    
class Friend(models.Model):
    ''' Encapsulate the data of a friend relationship.'''

    # Define the data attributes of the Friend object
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile2')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        ''' Return a string representation of this model instance.'''
        return f'{self.profile1} is friends with {self.profile2}'  