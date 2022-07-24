from django.db import models
from django.conf import settings


class ShortURL(models.Model):
    long_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=255)
    full_url = models.CharField(max_length=255, default="/")
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.short_url
