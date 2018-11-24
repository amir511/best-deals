from django.utils.decorators import method_decorator
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product
from .serializers import ProductSerializer

PLATFORM_PARAM = openapi.Parameter('platform', openapi.IN_QUERY, description="filter by platform (jumia or souq)", type=openapi.TYPE_STRING)
BRAND_PARAM = openapi.Parameter('brand', openapi.IN_QUERY, description="filter by brand", type=openapi.TYPE_STRING)
SEARCH_PARAM = openapi.Parameter('search', openapi.IN_QUERY, description="search the description of the products", type=openapi.TYPE_STRING)
MAX_PRICE_PARAM = openapi.Parameter('max_price', openapi.IN_QUERY, description="excludes products that has prices above this number", type=openapi.TYPE_NUMBER)
MIN_PRICE_PARAM = openapi.Parameter('min_price', openapi.IN_QUERY, description="excludes products that has prices below this number", type=openapi.TYPE_NUMBER)
SORT_PARAM = openapi.Parameter('sort', openapi.IN_QUERY, description="sorts products either ascending or descending based on prices, accepts `a` or `d`", type=openapi.TYPE_STRING)

PARAM_LIST = [
    PLATFORM_PARAM,
    BRAND_PARAM,
    SEARCH_PARAM,
    MAX_PRICE_PARAM,
    MIN_PRICE_PARAM,
    SORT_PARAM,
]

@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=PARAM_LIST))
class ProductViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Returns the specified product
    ---
    list:
    Returns a list of all products
    ---
    """
    serializer_class = ProductSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Product.objects.all().order_by('description')
        platform = self.request.query_params.get('platform', None)
        brand = self.request.query_params.get('brand', None)
        search = self.request.query_params.get('search', None)
        max_price = self.request.query_params.get('max_price', None)
        min_price = self.request.query_params.get('min_price', None)
        sort = self.request.query_params.get('sort', None)
        
        if platform:
            queryset = queryset.filter(platform__icontains=platform).order_by('description')
        if brand:
            queryset = queryset.filter(brand__icontains=brand).order_by('description')
        if search:
            queryset = queryset.filter(description__search=search).order_by('description')
        if max_price:
            queryset = queryset.exclude(new_price__gt=max_price).order_by('description')
        if min_price:
            queryset = queryset.exclude(new_price__lt=min_price).order_by('description')
        if sort:
            if sort == 'a':
                queryset = queryset.order_by('new_price')
            elif sort == 'd':
                queryset = queryset.order_by('-new_price')

        return queryset
