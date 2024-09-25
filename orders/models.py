import uuid
from django.db import models
from products.models import Product
from customers.models import Customer

class Order(models.Model):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    customer=models.ForeignKey(
        Customer,
        related_name="orders",
        on_delete=models.DO_NOTHING
    )
    products=models.ManyToManyField(
        Product,
        related_name="orders",
    )
    delivered=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer}"