# File: models.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 04/15/2025
# Description: This file contains the model for the Project objects.
from django.db import models #type: ignore
from django.contrib.auth.models import User as AuthUser # type: ignore

# Create your models here.
class Tag(models.Model):
    # Represents interests, genres, platforms, or roles.
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'
    
class Work(models.Model):
    # Represents a creator’s project or content.
    title = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=[
        ("Game", "Game"),
        ("Stream", "Stream"),
        ("Tool", "Tool"),
        ("Mod", "Mod")
    ])
    image = models.ImageField(upload_to='works/', blank=True, null=True)
    link = models.URLField()

    def __str__(self):
        return f'{self.title}'
    
class Profile(models.Model):
    # Represents a Black creator or streamer.
    PROFILE_TYPES = [
        ("Game Creator", "Game Creator"),
        ("Streamer", "Streamer"),
        ("Youtuber", "Youtuber"),
        ("Streamer/Youtuber", "Streamer/Youtuber"),
    ]

    name = models.CharField(max_length=100)
    profile_type = models.CharField(max_length=50, choices=PROFILE_TYPES)
    nationality = models.CharField(max_length=100)
    bio = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True)
    website_or_channel = models.URLField(blank=True, null=True)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    featured_works = models.ManyToManyField(Work, blank=True)
    date_added = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_creator_by = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_profiles')

    def __str__(self):
        return f'{self.name}'
    

class UserProfile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)
    bookmarked_profiles = models.ManyToManyField(Profile, blank=True, related_name='bookmarked_by')
    interests = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.user.username}'

class Submission(models.Model):
    # Represents a user-submitted creator profile pending review.
    submitted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    profile_type = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)
    bio = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True)
    website_or_channel = models.URLField(blank=True, null=True)
    reason_for_submission = models.TextField()
    photo = models.ImageField(upload_to='submissions/', blank=True, null=True)
    date_submitted = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    # Status of the submission
    STATUS_CHOICES = [
    ('pending', 'Pending Review'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Submission: {self.name} by {self.submitted_by.user.username}"
    
class WorkSubmission(models.Model):
    submitted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=[
        ("Game", "Game"),
        ("Stream", "Stream"),
        ("Tool", "Tool"),
        ("Mod", "Mod")
    ])
    image = models.ImageField(upload_to='submitted_works/', blank=True, null=True)
    link = models.URLField()
    approved = models.BooleanField(default=False)
    date_submitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.creator.name}"

