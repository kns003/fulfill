from django.db import models
from django.urls import reverse
from acme_core.models import AcmeBase

# Create your models here.

class Product(AcmeBase):
    """
    The main model which holds the data of Product
    """
    sku = models.CharField(max_length=200, null=True, blank=True)
    SOURCE = (
        ('csv', 'Csv'),
        ('app', 'App')
    )
    source = models.CharField(max_length=50, default='app', choices=SOURCE)

    class Meta:
        unique_together = ('name', 'description', 'sku')

    def get_absolute_url(self):
        return reverse('product-list')

class ProductUploadData(AcmeBase):
    """
    Model which contains file upload data
    """
    file = models.FileField(upload_to='upload/')
    success_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    total_count = models.PositiveIntegerField(default=0)

    def to_stream_dict(self):
        return {
            'success_count': self.success_count,
            'total_count': self.total_count,
            'percentage': str(int((self.success_count/self.total_count)*100))
            if self.total_count else 0
        }

class Webhook(AcmeBase):
    """
    Model to configure Webhook
    """
    url = models.URLField(null=True, blank=True)
    EVENT_CHOICE = (
        ('product_created', 'Product Created'),
        ('product_updated', 'Product Updated')
    )
    event = models.CharField(max_length=200, null=True, blank=True, choices=EVENT_CHOICE,
                             verbose_name='Event to be triggered at')

    class Meta:
        unique_together = ('url', 'event', 'name')

    def get_absolute_url(self):
        return reverse('webhook-list')