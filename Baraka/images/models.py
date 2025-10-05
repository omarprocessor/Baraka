from django.db import models
import uuid
import os


def upload_to(instance, filename):
    """Generate unique filename for uploaded images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('images', filename)


class ImageAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=upload_to)
    original_filename = models.CharField(max_length=255)
    analysis_result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.original_filename} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"