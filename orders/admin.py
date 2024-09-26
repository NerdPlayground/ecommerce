from .models import Order
from django.contrib import admin
from products.models import Product
from django.utils.html import format_html_join

class OrderAdmin(admin.ModelAdmin):
    list_display=[
        "id","customer","products_list",
        "delivered","created_on",
    ]
    search_fields=["id","customer__user__username"]

    def products_list(self,obj):
        contents=Product.objects.filter(orders=obj.id).values_list("name")
        return format_html_join(
            "\n","<li style='list-style-type:none;'>{}</li>",
            (content for content in contents)
        )

    def has_add_permission(self,request):
        return False

    def has_change_permission(self,request,obj=None):
        return False

    def has_delete_permission(self,request,obj=None):
        return False

admin.site.register(Order,OrderAdmin)
