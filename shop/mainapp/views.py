from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Notebook, Smartphone, Category, LatestProducts, Customer, Cart
from .mixins import CategoryDetailMixin
from django.http import HttpResponseRedirect

# Create your views here.

class BaseView(View):
    def get(self, requests, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page(
            'notebook', 'smartphone', with_respect_to='notebook'
        )
        print(f'products={products}')

        context = {'categories': categories,
                   'products': products,
                   }
        return render(requests, 'base.html', context)

# def test_view(requests):
#     categories = Category.objects.get_categories_for_left_sidebar()
#     return render(requests, 'base.html', {'categories': categories})



class ProductDetailView(CategoryDetailMixin, DetailView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context



class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()

    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'


class AddCartView(View):
    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        return HttpResponseRedirect('/cart/')

class CartView(View):

    def get(self, request, *args, **kwargs):
        # customer = Customer.objects.get(user=request.user)
        # cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories,
        }

        return render(request, 'cart.html', context)