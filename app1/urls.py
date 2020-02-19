from django.urls import path
from . import views

#url patterns is just a list of all urls supported by the app
urlpatterns = [
    path("", views.index),
    path("register", views.register),
    ] 