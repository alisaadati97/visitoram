from django.contrib import admin

from .models import *
# Register your models here.

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('number','date','author','product','get_supplier','quantity','get_total_price','is_sent','is_recieved','is_done')
    list_editable = ('quantity',)
    list_filter = ('product','is_done','is_sent')
    readonly_fields = ('number','date','author',)
    def get_supplier(self,obj):
        return obj.product.supplier
    
    def get_total_price(self,obj):
        try:
            return  f"{obj.cal_total_price():,}" + ' Rials'
        except:
            return None

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.values()[0]['name'] == 'supermarket':
            if not obj.is_done:
                return ('number','date','author','is_sent','is_recieved',)
            elif obj.is_done and not obj.is_sent:
                return ('number','date','author','is_sent','is_recieved','product','quantity','is_done')
            elif obj.is_done and  obj.is_sent and not obj.is_recieved:
                return ('number','date','author','is_sent','product','quantity','is_done')
            else : 
                return ('number','date','author','is_sent','is_recieved','product','quantity','is_done')
        
        elif request.user.groups.values()[0]['name'] == 'pakhsh':
            if obj.is_done and not obj.is_sent:
                return ('number','date','author','is_recieved','product','quantity','is_done')
            else:
                return ('number','date','author','is_sent','is_recieved','product','quantity','is_done')

        return self.readonly_fields

    def get_queryset(self, request): 
        qs = super(OrderItemAdmin, self).get_queryset(request) 
        if request.user.is_superuser:
            return qs.all()
        if request.user.groups.values()[0]['name'] == 'supermarket':
            print('super',self.list_editable)
            self.list_editable =  ('quantity',)
            return qs.filter(author=request.user)
        else :
            print('ssss',self.list_editable)
            self.list_editable = ()
            return qs.filter(product__supplier=request.user,is_done=True)
    

    def save_model(self, request, obj, form, change):
        if request.user.groups.values()[0]['name'] == 'supermarket':
            if obj.is_done and 'is_done' not in form.changed_data and 'is_recieved' not in form.changed_data :
                return
        if request.user.groups.values()[0]['name'] == 'pakhsh':
            if obj.is_done and 'is_sent' not in form.changed_data :
                return
        if not request.user.is_superuser:
            if request.user.groups.values()[0]['name'] == 'supermarket':
                obj.author = request.user
        obj.save()

admin.site.register(OrderItem , OrderItemAdmin)