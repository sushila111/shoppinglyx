from django.contrib import admin
from django.utils.html import format_html
from app.models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)
# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','user','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','description',
    'brand','category']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
  list_display = ['id', 'user','customer','product',
  'quantity','ordered_date','status']


def customer_infro(self,obj):
    link = reverse("admin:app_customer_change",agrs=[obj.customer.pk])
    return format_html('<a href="{}">{}</a>', link, obj.customer.name)