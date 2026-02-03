# Create your models here.
from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume_file = models.FileField(upload_to='resumes/')#upload folder
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills_required = models.TextField()#comma sepearted value
    role = models.CharField(max_length=100)






    def __str__(self):
        return self.title
