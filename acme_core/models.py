from django.db import models
from .model_manager import AcmeBaseManager

# Create your models here.
class AcmeBase(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    objects = AcmeBaseManager()

    class Meta:
        abstract = True