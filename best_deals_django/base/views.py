from .models import Product
from rest_framework import viewsets
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
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

