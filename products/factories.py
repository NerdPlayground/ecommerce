import factory
from datetime import date
from .models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Product
    
    name=factory.Faker("word")
    price=factory.Faker("random_number",digits=4,fix_len=True)