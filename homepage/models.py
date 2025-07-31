from django.db import models
from django.conf import settings

class SerialRecord(models.Model):
    serial_number = models.CharField(max_length=100)
    worker_name   = models.CharField(   # the name read from the image
        max_length=100
    )
    uploader      = models.ForeignKey(  # the logged-in user who uploads worker_name
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploads"
    )
    processed_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.serial_number} by {self.worker_name}"
