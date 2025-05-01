# File: urls.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 04/18/2025
# Description: Urls for each template page of the project app.

from django.urls import path # type: ignore
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profiles/', ProfileListView.as_view(), name='profile_list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('submit/', CreateProfileView.as_view(), name='submit_profile'),
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('chatbot/', views.GeminiChatbotView.as_view(), name='chatbot'),
    path('chatbot/clear/', views.clear_chat_history, name='clear_chat_history'),
    path('chatbot/delete/<int:index>/', views.delete_chat_entry, name='delete_chat_entry'),
    path('bookmarks/', views.BookmarkedProfilesView.as_view(), name='bookmarked_profiles'),
    path('bookmark/<int:pk>/', views.ToggleBookmarkView.as_view(), name='toggle_bookmark'),
    path('account/', views.UserProfileView.as_view(), name='user_profile'),
    path('account/edit/', views.EditUserProfileView.as_view(), name='edit_user_profile'),
    path('profiles/<int:pk>/edit/', views.EditCreatorProfileView.as_view(), name='edit_creator'),
    path('submit-work/', views.SubmitWorkView.as_view(), name='submit_work'),

    #authorization-related URLs:
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logout.html'), name='logout'), 
    path('signup/', SignupView.as_view(), name='signup'),
]