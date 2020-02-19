from django.contrib import admin
from .models import Tweet, User

# Register your models here with the built in admin site.  
# use the command python manage.py createsuperuser
# login at website/admin to be able to adjust all the databases

admin.site.register(Tweet)
admin.site.register(User)