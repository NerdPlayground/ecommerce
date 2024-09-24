from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer
from django.contrib.auth.models import User

class CustomerInline(admin.StackedInline):
    model=Customer

class CustomUserAdmin(UserAdmin):
    inlines=[CustomerInline]

admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)