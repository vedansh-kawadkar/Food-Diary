from django.db import models

# Create your models here.
class UploadCSV_new(models.Model):
    filename = models.FileField()

    def __str__(self):
        return self.filename
