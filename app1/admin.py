from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Tweet, Profile
# Register your models here with the built in admin site.  
# use the command python manage.py createsuperuser
# login at website/admin to be able to adjust all the databases

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"
    
#Define a new user admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


#re-register useradmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tweet)