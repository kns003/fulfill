import requests
import json
from django.db.models.signals import post_save
from django.forms import model_to_dict
from django.dispatch import receiver
from .models import Product, Webhook
from .tasks import post_webhook

@receiver(post_save, sender=Product)
def trigger_webhook(sender, instance, created, **kwargs):
    if instance.source == 'app':
        if created:
            event = 'product_created'
        else:
            event = 'product_updated'
        # get all webhooks for product creation
        webhooks = Webhook.objects.filter(is_active=True, event=event)
        for webhook in webhooks:
            print('Triggering {} webhook with following data : {} on the url {} \n\n'.format(
                event, str(model_to_dict(instance)), str(webhook.url)))
            post_webhook.delay(webhook.id, instance.id)