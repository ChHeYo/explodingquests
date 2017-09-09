from django.contrib import admin

from .models import WorkExperience, Education, DefuseMessage


class DefuseMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'subject', 'content', 'viewed_by_receiver')

# Register your models here.

admin.site.register(WorkExperience)
admin.site.register(Education)
admin.site.register(DefuseMessage, DefuseMessageAdmin)
