# File: urls.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/20/2025
# Description: Urls for each template page of the web app
from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView
from . import views

urlpatterns = [
    # URL pattern for the all_profiles page.
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    # URL pattern for each singular profile page.
    path('Profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
]