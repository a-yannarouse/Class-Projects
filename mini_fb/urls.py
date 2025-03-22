# File: urls.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/20/2025
# Description: Urls for each template page of the web app
from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusMessageView, AddFriendView, ShowFriendSuggestionsView, ShowNewsFeedView 

urlpatterns = [
    # URL pattern for the all_profiles page.
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    # URL pattern for each singular profile page.
    path('Profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('Profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('Profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    path('Status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('Status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'),
    path('Profile/<int:pk>/add_friend/<int:other_pk>', AddFriendView.as_view(), name='add_friend'),
    path('Profile/<int:pk>/suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('Profile/<int:pk>/news_feed', ShowNewsFeedView.as_view(), name='news_feed'),
]