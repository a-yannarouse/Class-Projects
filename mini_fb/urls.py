# mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfilesView
from . import views

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
]