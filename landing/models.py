import os
from django.db import models
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)

#file categorization
@deconstructible
class DynamicUploadPath:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1].lower()
        name = filename.lower()

        # Default folder
        folder = 'Others'

        if ext == 'pdf':
            folder = 'Application Form'
        elif ext in ['doc', 'docx']:
            folder = 'Request Letter'
        elif any(keyword in name for keyword in ['signature', 'sign', 'e-sign', 'esign']):
            folder = 'Signature Images'
        elif ext in ['jpg', 'jpeg', 'png', 'gif', 'jfif'] and any(k in name for k in ['id', 'identification']):
            folder = 'Identification Images'

        logger.debug(f"Uploading {filename} to folder: {folder}")

        instance.folder = folder
        instance.file_type = ext
        return os.path.join(folder, filename)

upload_path = DynamicUploadPath()


class File(models.Model):
    file = models.FileField(upload_to=upload_path)
    folder = models.CharField(max_length=255, blank=True)
    file_type = models.CharField(max_length=50, blank=True)  # avoids migration error


class Folder(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

#baranggay monitoring
class Barangay(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Incomplete', 'Incomplete'),
    ]

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    due_date = models.DateField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True)
    certificates_issued = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def performance_score(self):
        """Calculate performance score based on status and timeliness"""
        if self.status == 'Completed':
            return 95
        elif self.status == 'Pending':
            return 87
        else:
            return 60
    
# Employee Model for Employee Profile Management
class Employee(models.Model):
    TASK_CHOICES = [
        ('Monitoring', 'Monitoring'),
        ('Documentation', 'Documentation'),
        ('Analysis', 'Analysis'),
        ('Support', 'Support'),
    ]
    
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    task_assign = models.CharField(max_length=50, choices=TASK_CHOICES, default='Monitoring')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.employee_id}"




