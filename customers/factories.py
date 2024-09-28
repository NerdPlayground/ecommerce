import factory
from decouple import config
from .models import Customer
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=get_user_model()
    
    @factory.lazy_attribute
    def username(self):
        simple_profile=factory.Faker("simple_profile")
        result=simple_profile.evaluate(None,None,{"locale": None})
        return f"{result.get('username')}-{self.first_name}".lower()

    first_name=factory.Faker("first_name")
    last_name=factory.Faker("last_name")
    email=factory.LazyAttribute(lambda e: "{}@gmail.com".format(e.username).lower())
    password=factory.django.Password("qwerty123!@#")

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Customer

    user=factory.SubFactory(UserFactory)
    phone_number=config("AT_PHONE_NUMBER")