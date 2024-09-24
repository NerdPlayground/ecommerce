from rest_framework import serializers
from .models import Customer
from django.contrib.auth import get_user_model

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True,allow_blank=False)
    password=serializers.CharField(style={'input_type': 'password'})

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=["phone_number"]

class UserSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer()

    class Meta:
        model=get_user_model()
        fields=["username","first_name","last_name","email","customer"]
    
    def update(self,instance,validated_data):
        customer=Customer.objects.get(user=instance)
        customer_data=validated_data.pop("customer")
        customer.phone_number=customer_data["phone_number"]
        customer.save()

        instance.username=validated_data["username"]
        instance.first_name=validated_data["first_name"]
        instance.last_name=validated_data["last_name"]
        instance.email=validated_data["email"]
        instance.save()