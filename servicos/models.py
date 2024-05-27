from secrets import token_hex
from django.db import models
from clientes.models import Cliente, Pet
from .choices import ChoicesCategory
from datetime import datetime

class Category(models.Model):
    title = models.CharField(max_length=3, choices=ChoicesCategory.choices)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self) -> str:
        return self.title

class Services(models.Model):
    title = models.CharField(max_length=30)
    client = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    service_category = models.ManyToManyField(Category)
    
    date_init = models.DateTimeField(null=True)
    date_final = models.DateTimeField(null=True)
    finished = models.BooleanField(default=False)
    protocol = models.CharField(max_length=32, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.protocol:
            self.protocol = datetime.now().strftime("%d/%m/%Y-%H:%M:%S-") + token_hex(5)
        super(Services, self).save(*args, **kwargs)
        
    def total_price(self):
        total_price = float(0)
        for cat in self.service_category.all():
            total_price += float(cat.price)
        return total_price