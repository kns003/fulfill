from django.urls import path
from django.views.generic import TemplateView
from .views import HandleProductUpload, CheckProdStatus, ProductList, \
    ProductCreate, ProductEdit, ProductDelete, WebhookList, WebhookAdd, \
    WebhookUpdate, ProductDeleteAll

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('upload/', HandleProductUpload.as_view(), name='upload'),
    path('status/<int:upload_id>/', CheckProdStatus.as_view(), name='status'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/create/', ProductCreate.as_view(), name='product-create'),
    path('products/delete-all/', ProductDeleteAll.as_view(), name='product-delete-all'),
    path('products/<int:product_id>/', ProductEdit.as_view(), name='product-update'),
    path('products/<int:product_id>/delete/', ProductDelete.as_view(), name='product-delete'),
    path('products/webhooks/', WebhookList.as_view(), name='webhook-list'),
    path('products/webhooks/add/', WebhookAdd.as_view(), name='webhook-add'),
    path('products/webhooks/<int:webhook_id>/', WebhookUpdate.as_view(), name='webhook-update')
]