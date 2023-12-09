# sharedfile.py
from django.db import models
from django.contrib.auth.models import User
from .models import UploadedFile

class SharedFile(models.Model):
    user_shared_from = models.ForeignKey(User, related_name='shared_files_sent', on_delete=models.CASCADE)
    user_shared_with = models.ForeignKey(User, related_name='shared_files_received', on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
