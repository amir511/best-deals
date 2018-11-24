from django.db import models


class Product(models.Model):
    product_id = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.CharField(max_length=255)
    link = models.URLField(max_length=450)
    old_price = models.CharField(max_length=255)
    new_price = models.CharField(max_length=255)
    image = models.URLField(max_length=450)
    platform = models.CharField(max_length=255)

    def __str__(self):
        return self.platform + ":" + self.description

