import os
from django.db import models
from django.utils.deconstruct import deconstructible

@deconstructible
class DynamicUploadPath:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1].lower()
        name = filename.lower()

        if ext == 'pdf':
            folder = 'Application Form'
        elif ext in ['doc', 'docx']:  # <-- simplified this line
            folder = 'Request Letter'
        if any(keyword in name for keyword in ['signature', 'sign', 'e-sign', 'esign']):
            folder = 'Signature Images'
        elif ext in ['jpg', 'jpeg', 'png', 'gif','jfif'] and any(k in name for k in ['id', 'identification']):
            folder = 'Identification Images'
    

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
