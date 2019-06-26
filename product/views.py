from django.urls import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse
from .models import ProductUploadData, Product, Webhook
from .tasks import AsyncFileUploaTask


class HandleProductUpload(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(HandleProductUpload, self).dispatch(request, *args, **kwargs)

    def save_product_data(self, file):
        prod = ProductUploadData.objects.create(
            file=file
        )
        return prod.id

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        prod_id = self.save_product_data(file)
        AsyncFileUploaTask().delay(
            prod_id=prod_id
        )
        return JsonResponse(
            {'status': True,
             'msg': "File Uploaded for processing",
             'file_upload_id': prod_id}
        )

class CheckProdStatus(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CheckProdStatus, self).dispatch(request, *args, **kwargs)

    def get(self, request, upload_id, *args, **kwargs):
        try:
            prod_up = ProductUploadData.objects.get(id=upload_id)
        except:
            pass

        ret_data = "data: {}\n\n".format(prod_up.to_stream_dict().get('percentage'))
        return HttpResponse(ret_data,
                            content_type='text/event-stream')


class ProductList(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        search_val = self.request.GET.get('q', '')
        is_active = self.request.GET.get('is_active', 'true')
        is_active = True if is_active == 'true' else False
        object_list = Product.objects.filter(is_active=is_active).order_by('-modified_at')
        if search_val:
            object_list = object_list.filter(
                Q(name__icontains=search_val)|Q(description__icontains=search_val))
        return object_list

class ProductCreate(CreateView):
    model = Product
    template_name = 'product_create.html'
    fields = ['name', 'description', 'sku']

class ProductEdit(UpdateView):
    model = Product
    template_name = 'product_update.html'
    fields = ['name', 'description', 'sku']
    pk_url_kwarg = 'product_id'

    def get_initial(self):
        initial = super(ProductEdit, self).get_initial()
        product = self.get_object()
        initial['name'] = product.name
        initial['description'] = product.description
        initial['sku'] = product.sku
        return initial

    def get_object(self, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        return product

class ProductDelete(DeleteView):
    model = Product
    template_name = 'product_delete_confirmation.html'
    success_url = reverse_lazy('product-list')
    pk_url_kwarg = 'product_id'

class WebhookList(ListView):
    model = Webhook
    template_name = 'webhook_list.html'
    context_object_name = 'webhooks'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WebhookList, self).dispatch(request, *args, **kwargs)

class WebhookAdd(CreateView):
    model = Webhook
    template_name = 'webhook_create.html'
    fields = ['name', 'description', 'url', 'event', 'is_active']

class WebhookUpdate(UpdateView):
    model = Webhook
    template_name = 'webhook_update.html'
    fields = ['name', 'description', 'url', 'event', 'is_active']
    pk_url_kwarg = 'webhook_id'

    def get_initial(self):
        initial = super(WebhookUpdate, self).get_initial()
        webhook = self.get_object()
        initial['name'] = webhook.name
        initial['description'] = webhook.description
        initial['url'] = webhook.url
        initial['event'] = webhook.event
        return initial

    def get_object(self, *args, **kwargs):
        webhook = get_object_or_404(Webhook, pk=self.kwargs['webhook_id'])
        return webhook




