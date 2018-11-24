from .models import Product
from rest_framework import viewsets
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    http_method_names = ['get']

    def get_queryset(self):
        queryset = Product.objects.all().order_by('description')
        platform = self.request.query_params.get('platform', None)
        search = self.request.query_params.get('search', None)
        if platform:
            queryset = queryset.filter(platform=platform.capitalize())
        if search:
            queryset = queryset.filter(description__search=search)
        return queryset

