# File: urls.py
# Author: A'Yanna Rouse (yanni620@bu.edu), 02/11/2025
# Description: Urls for each template page of the web app
from django.urls import path
from . import views

# URL pattern for the app
urlpatterns = [
    # URL pattern for the main page.
    path(r'main', views.main_page, name="main"),
    # URL pattern for the order page.
    path(r'order', views.order_page, name="order"),
    # URL pattern for the confirmation page; uses the 'submit' view to process order submissions.
    path(r'confirmation', views.submit, name="confirmation"),
]