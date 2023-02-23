from django.contrib import admin

from .models import *
from supermarket.models import *
import decimal

# Register your models here.
# from django.contrib.admin.models import LogEntry
# admin.site.register(LogEntry)

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(ProductType, ProductTypeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description','supplier','get_price','address')
    list_filter = ('type',)
    readonly_fields = ('number','supplier',)
    actions = ['add_to_basket']
    def has_group(self,request):
        if len(request.user.groups.values()) == 0:
            return False
        return True
         

    def get_price(self,obj):
        try:
            return  f"{obj.unit_price:,}" + ' Rials'
        except:
            return None
    def add_to_basket(self, request, queryset):
        for item in queryset:
            OrderItem.objects.create(product=item,author=request.user)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not self.has_group(request):
            return None
        group_name = request.user.groups.values()[0]['name']
        if  group_name == 'supermarket':
            return actions
        elif group_name == 'pakhsh':
            return None
    
    def get_queryset(self, request): 
        qs = super(ProductAdmin, self).get_queryset(request) 
        if request.user.is_superuser:
            return qs.all()
        if not self.has_group(request):
            return None
        group_name = request.user.groups.values()[0]['name']
        if group_name == 'supermarket':
            decimal.getcontext().prec = 6
            params = [request.user.long + decimal.Decimal(0.01) ,request.user.long - decimal.Decimal(0.01) ,
                        request.user.lat + decimal.Decimal(0.01) ,request.user.lat - decimal.Decimal(0.01)  ]

            return qs.filter(supplier__long__lte = params[0],supplier__long__gte = params[1],
            supplier__lat__lte = params[2],supplier__lat__gte = params[3] )
        elif group_name == 'pakhsh' :
            return qs.filter(supplier=request.user)
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.supplier = request.user
        obj.save()

admin.site.register(Product, ProductAdmin)
