from django.contrib import admin

from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group
from .models import Product,Customer,Cart,Payment,OrderPlaced,Wishlist,ProductCategory,ProductVariation
# Register your models here.


@admin.register(ProductCategory)
class ProductCategoryModelAdmin(admin.ModelAdmin):
    # prepopulated_fields={'slug':('name',)}       
    list_display=['id','name','slug']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)} 
    list_display = ['id','title','discounted_price','category','product_image','stock_quantity']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','mobile','pincode']

@admin.register(ProductVariation)
class ProductVariationModelAdmin(admin.ModelAdmin):
    list_display = ['id','product','quantity','selling_price','discounted_price']





@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','products','quantity']
    def products(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}" > {} </a>',link,obj.product.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customers','products','quantity','ordereded_date','status','payments']
    def products(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}" > {} </a>',link,obj.product.title)
    def customers(self,obj):
        link = reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}" > {} </a>',link,obj.customer.name)
    def payments(self,obj):
        link = reverse("admin:app_payment_change",args=[obj.payment.pk])
        return format_html('<a href="{}" > {} </a>',link,obj.payment.razorpay_payment_id)

        

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display=['id','user','products']
    def products(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}" > {} </a>',link,obj.product.title)

admin.site.unregister(Group)