# File: admin.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 04/18/2025
# Description: This file contains the admin settings for the project models. 

from django.contrib import admin
from .models import Submission, Profile, Tag, Work, UserProfile

@admin.action(description='Create Profile(s) from approved Submission(s)')

def create_profiles_from_submissions(modeladmin, request, queryset):
    created = 0
    skipped = 0

    for submission in queryset:
        if submission.status == 'approved':
            profile, created_flag = Profile.objects.get_or_create(
                name=submission.name,
                defaults={
                    'profile_type': submission.profile_type,
                    'nationality': submission.nationality,
                    'bio': submission.bio,
                    'location': submission.location,
                    'website_or_channel': submission.website_or_channel,
                    'photo': submission.photo,
                }
            )
            if created_flag:
                profile.tags.set(submission.tags.all())  
                profile.created_by = submission.submitted_by.user 
                profile.photo = submission.photo 
                profile.save()

                created += 1
                submission.delete()  # auto-delete submission after success
            else:
                skipped += 1

        else:
            skipped += 1

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    actions = [create_profiles_from_submissions]

admin.site.register(Profile)

admin.site.register(Tag)
admin.site.register(Work)
admin.site.register(UserProfile)