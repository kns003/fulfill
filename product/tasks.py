import csv
import json
import requests
from celery import Task
from celery import task
from django.db.models import F
from django.forms import model_to_dict
from acme.celery import app
from .models import ProductUploadData, Product, Webhook


class AsyncFileUploaTask(Task):
    """
    Task which is used to upload the file in async way
    """
    name = "async_file_upload_task"

    def run(self, **kwargs):
        try:
            # get objects from kwargs
            self.file_upload_obj = self._get_required_objs_from_kwargs(**kwargs)
            print(self.file_upload_obj)
            file = self.file_upload_obj.file
            self._read_csv_file(file)
        except Exception as exception:
            msg = "Exception occurred while validating uploaded file : {}".format(str(exception))
            raise Exception(msg)

    def _get_required_objs_from_kwargs(self, **kwargs):
        try:
            return ProductUploadData.objects.get(id=kwargs.get('prod_id'))
        except ProductUploadData.DoesNotExist:
            return None

    def _create_product_entry(self, obj):
        print('_create_product_entry')
        prod, _ = Product.objects.get_or_create(
            sku=obj.get('sku'),
        )
        prod.name = obj.get('name')
        prod.description = obj.get('description')
        prod.source = 'csv'
        prod.save()

    def _update_row_count(self, success):
        print('_update_row_count')
        if success:
            self.file_upload_obj.success_count = F('success_count') + 1
        else:
            self.file_upload_obj.failed_count = F('failed_count') + 1
        self.file_upload_obj.save()

    def _read_csv_file(self, file):
        reader = csv.DictReader(open(file.path))
        self.file_upload_obj.total_count = len(list(reader))
        self.file_upload_obj.save()
        reader = csv.DictReader(open(file.path))
        for obj in reader:
            import time
            time.sleep(1)
            try:
                self._create_product_entry(obj)
            except:
                self._update_row_count(False)
                continue
            self._update_row_count(True)


app.tasks.register(AsyncFileUploaTask())

@task
def post_webhook(webhook_id, instance_id):
    webhook = Webhook.objects.get(id=webhook_id)
    instance = Product.objects.get(id=instance_id)
    try:
        requests.post(webhook.url, json.dumps(model_to_dict(instance)))
    except:
        pass
