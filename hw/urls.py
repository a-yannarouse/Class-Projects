from django.urls import path
from . import views

urlpatterns = [ 
    path(r'', views.home_page, name="home_page"),
    path(r'about', views.about_page, name="about_page"),
]