import uuid
from django.db import models

class Product(models.Model):
    id= models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name=models.CharField(max_length=255)
    price=models.IntegerField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product-detail",kwargs={"pk":self.id})
    
    class Meta:
        ordering=["-created_on"]