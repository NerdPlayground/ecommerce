from .models import Product
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    list_display=["id","name","price","created_on"]
    search_fields=["name"]

admin.site.register(Product,ProductAdmin)