from django.urls import path
from .views import upload_resume, success
from . import views
urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('success/', success, name='success'),
]
