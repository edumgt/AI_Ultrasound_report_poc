from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/upload-audio/", views.upload_audio, name="upload_audio"),
]
