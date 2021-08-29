from django.shortcuts import render
from django.views.generic import DetailView
from .models import Notebook, Smartphone

# Create your views here.

def test_view(requests):
    return render(requests, 'base.html')



class ProductDetailView(DetailView):
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone,
    }

    # Вытаскиваем из slug название модели и в зависимости от нее определяем модель товара
    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'