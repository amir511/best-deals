from .models import Product
from rest_framework import viewsets
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('description')
    serializer_class = ProductSerializer
    http_method_names = ['get']

class ProductByPlatform(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    http_method_names = ['get']

    def get_queryset(self):
        platform = self.kwargs['platform']
        return Product.objects.filter(platform=platform).order_by('description')
