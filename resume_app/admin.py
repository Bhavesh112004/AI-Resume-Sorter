from django.contrib import admin
from .models import Resume, Job
from django.utils.html import format_html # Modern replacement for allow_tags

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_resume')

    def get_resume(self, obj):
        if obj.resume_file:
            # Replaced deprecated allow_tags with format_html
            return format_html('<a href="{}" target="_blank">Download Resume</a>', obj.resume_file.url)
        return "No Resume Uploaded"
    get_resume.short_description = 'Uploaded Resume'

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    # Changed 'required_skills' to 'skills_required' to match models.py
    list_display = ("title", "role")
    search_fields = ("title", "skills_required", "role")