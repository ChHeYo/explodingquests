from django.contrib import admin

from .models import WorkExperience, Education, DefuseMessage


class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'title',
    )
    list_display_links = ('title', )


class DefuseMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sender',
        'receiver', 'subject',
        'content', 'viewed_by_receiver')
    list_display_links = ('subject', )

# Register your models here.

admin.site.register(WorkExperience, ExperienceAdmin)
admin.site.register(Education)
admin.site.register(DefuseMessage, DefuseMessageAdmin)
