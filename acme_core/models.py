from django.db import models

# Create your models here.
class AcmeBase(models.Model):
    """
    This is a Base model which can be used to extend in all the models
    """
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True