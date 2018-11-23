from django.db import models


class Product(models.Model):
    class Meta:
        unique_together = ('product_id', 'platform')

    product_id = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    link = models.URLField()
    old_price = models.CharField(max_length=255)
    new_price = models.CharField(max_length=255)
    image = models.URLField()
    platform = models.CharField(max_length=255)

    def __str__(self):
        return self.platform + ":" + self.description

