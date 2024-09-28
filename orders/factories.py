import factory
from .models import Order
from django.db.models.signals import post_save

@factory.django.mute_signals(post_save)
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Order
    
    @factory.post_generation
    def products(self,created,extracted,**kwargs):
        if not created or not extracted: return
        self.products.add(*extracted)