from django.db import models

from django.shortcuts import reverse


CATEGORY_CHOICES = (
    ('DR', 'Drink ware'),
    ('YG', 'Yoga Store'),
    ('CA', 'Clothing & Accessories')
)


AVAILABILITY_PRODUCT = (
    ('S', 'In Stock'),
    ('0', 'Out Of Range')
)

class Product(models.Model):

    name = models.CharField(max_length=150)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    description = models.TextField()
    availabily = models.CharField(
        choices=AVAILABILITY_PRODUCT, max_length=1, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    
    

    def __str__(self):
        return self.name

