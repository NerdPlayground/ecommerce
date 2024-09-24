from django.db import models
from django.contrib.auth import get_user_model

class Customer(models.Model):
    user=models.OneToOneField(
        get_user_model(),
        primary_key=True,
        on_delete=models.CASCADE,
    )
    phone_number=models.CharField(max_length=13,null=True,blank=True)

    def __str__(self):
        full_name=self.user.get_full_name()
        return full_name if full_name!="" else self.user.username