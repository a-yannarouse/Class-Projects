# File: urls.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/20/2025
# Description: Urls for each template page of the web app
from django.urls import path # type: ignore
from .views import *
from . import views
from django.contrib.auth import views as auth_views # type: ignore

urlpatterns = [
    # URL pattern for the all_profiles page.
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    # URL pattern for each singular profile page.
    path('Profile', ShowProfilePageView.as_view(), name='show_profile'),
    path('Profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_other_profile'),  # Other profiles
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('Profile/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('Profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('Status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('Status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update_status'),
    path('Profile/add_friend/<int:other_pk>', AddFriendView.as_view(), name='add_friend'),
    path('Profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('Profile/news_feed', ShowNewsFeedView.as_view(), name='news_feed'),
    #authorization-related URLs:
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), 
]