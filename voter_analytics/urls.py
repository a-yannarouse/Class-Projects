# File: urls.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 03/31/2025
# Description: These are for the urls for the voter_analytics app.
from django.urls import path
from . import views 

urlpatterns = [
	path(r'', views.VoterListView.as_view(), name='voters_home'),
    path(r'voter', views.VoterListView.as_view(), name='voters_list'),
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name='voters_detail'),
    path(r'graphs', views.VoterGraphsView.as_view(), name='graphs'),
]