# File: views.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/20/2025
# Description: These are for the views for the mini_fb app, to show the profiles.
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.
class ShowAllProfilesView(ListView):
    ''' Define a view class to show all blog articles. '''
    # Defines the model, template, and context object name for the all profiles page
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "Profiles"

class ShowProfilePageView(DetailView):
    ''' Define a view class to show all blog articles. '''
    # Defines the model, template, and context object name for the singular profile page
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "Profile"
