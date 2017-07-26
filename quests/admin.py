from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Quest, UserProfile, Upload

# Register your models here.


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )    


class UploadAdmin(admin.ModelAdmin):
    list_display = ('quest',)
    list_display_links = ('quest',)
# class Profile

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Quest)
admin.site.register(Upload, UploadAdmin)
