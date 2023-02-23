from django.db import models
from user.models import User

# Create your models here.
class ProductType(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f'{self.name}'
    class Meta:
        ordering = ('-id',)

class Product(models.Model):
    number = models.PositiveIntegerField(blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)

    unit_price = models.PositiveIntegerField(blank=True,null=True)
    moq = models.PositiveIntegerField(blank=True,null=True,default=1)

    type = models.ForeignKey(ProductType , on_delete=models.CASCADE,blank=True,null=True)
    supplier = models.ForeignKey(User , on_delete=models.CASCADE,blank=True,null=True)
    address =  models.CharField(max_length=100,blank=True,null=True)
    
    image = models.ImageField(upload_to='',null=True)

    def __str__(self):
        return f'{self.supplier} - {self.name}'
    class Meta:
        ordering = ('-id',)
    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.number = Product.objects.all()[0].number + 1
            except:
                self.number = 1
        super(Product, self).save(*args, **kwargs)