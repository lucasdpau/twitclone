from django.urls import path

from . import views  #imports views.py from current directory

urlpatterns = [
    path("", views.index)  #the function named views in the module views.py
    ]