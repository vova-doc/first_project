from datetime import datetime

from django.db import models


class Post(models.Model):
    title = models.TextField(unique=True)
    content = models.TextField(null=True, blank=True) # контент будет нулабельный
    created_at = models.DateTimeField(default=datetime.now)
    visible = models.BooleanField(default=False)

    def __str__(self):
        msg = f"{self.title}, visible? {self.visible}"
        return msg


