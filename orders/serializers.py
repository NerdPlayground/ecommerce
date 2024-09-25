from .models import Order
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=[
            "id","customer","products",
            "delivered","created_on",
        ]
        read_only_fields=["customer","delivered"]

class DeliverSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=["delivered"]