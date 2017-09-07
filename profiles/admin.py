from django.contrib import admin

from .models import WorkExperience, Education, DefuseMessage

# Register your models here.

admin.site.register(WorkExperience)
admin.site.register(Education)
admin.site.register(DefuseMessage)
