from django.db import models
from pakhsh.models import Product
from user.models import User
from django.core.exceptions import ValidationError

import jdatetime

def set_persian_date():
    return jdatetime.datetime.now().strftime('%Y-%m-%d')

# Create your models here.


class OrderItem(models.Model):
    number  = models.PositiveIntegerField(blank=True,null=True)
    date = models.CharField(max_length=100,blank=True,null=True,default=set_persian_date)
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    quantity = models.PositiveIntegerField(blank=True,null=True)
    product = models.ForeignKey(Product , on_delete=models.CASCADE,blank=True,null=True)

    is_sent = models.BooleanField(default=False,blank=True,null=True)
    is_recieved = models.BooleanField(default=False,blank=True,null=True)
    is_done = models.BooleanField(default=False,blank=True,null=True)
    
    def cal_total_price(self):
        return self.quantity * self.product.unit_price
    
    def __str__(self):
        return f'{self.id}'
    
    class Meta:
        ordering = ('-id',)
    def clean(self, exclude=None):
        if self.product.moq != None and self.quantity < self.product.moq :
            raise ValidationError({'quantity': f"Not A Valid Quantity, should be at least {self.product.moq} items"})
    def save(self, *args, **kwargs):
        print()
        
        if not self.id:
            try:
                self.number = OrderItem.objects.all()[0].number + 1
            except:
                self.number = 1
        super(OrderItem, self).save(*args, **kwargs)
