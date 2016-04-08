from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=127)
    product_id = models.IntegerField(primary_key=True)


class Ecommerce(models.Model):
    ecomm_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=127)
    products = models.ManyToManyField(Product, through='Offerings')


class Offerings(models.Model):
    ecommerce = models.ForeignKey(Ecommerce, related_name='offerings')
    product = models.ForeignKey(Product, related_name='offerings')
    price = models.FloatField()
    url = models.URLField()
    last_modified = models.DateTimeField()

    class Meta:
        unique_together = ('ecommerce', 'product')
