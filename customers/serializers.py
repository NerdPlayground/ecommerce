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
        if validated_data.get("customer",None):
            customer=Customer.objects.get(user=instance)
            customer_data=validated_data["customer"]
            customer.phone_number=customer_data["phone_number"]
            customer.save()

        if validated_data.get("username",None):
            instance.username=validated_data["username"]
        if validated_data.get("first_name",None):
            instance.first_name=validated_data["first_name"]
        if validated_data.get("last_name",None):
            instance.last_name=validated_data["last_name"]
        if validated_data.get("email",None):
            instance.email=validated_data["email"]
        
        instance.save()
        return instance