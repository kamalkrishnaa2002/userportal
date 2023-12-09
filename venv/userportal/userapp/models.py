# models.py
from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class SharedFile(models.Model):
    user_shared_from = models.ForeignKey(User, related_name='shared_files_sent', on_delete=models.CASCADE)
    user_shared_with = models.ForeignKey(User, related_name='shared_files_received', on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
