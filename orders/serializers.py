from .models import Order
from .signals import deliver_order
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
    
    def update(self,instance,validated_data):
        response=super().update(instance,validated_data)
        deliver_order.send_robust(Order,instance=instance)
        return response