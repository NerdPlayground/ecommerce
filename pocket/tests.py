from django.urls import reverse
from django.test import TestCase
from products.factories import ProductFactory
from customers.factories import CustomerFactory

class PocketTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password="qwerty123!@#"
        cls.admin=CustomerFactory.create(user__is_staff=True)
        cls.member,cls.intruder=CustomerFactory.create_batch(2)
        cls.products=ProductFactory.create_batch(10)

    def member_login(self,member,password=None):
        password=password or self.password
        response=self.client.post(reverse("knox_login"),{
            "password":password,
            "username":member.user.username,
        })
        self.assertEqual(response.status_code,200)
        return response.json().get("token")

    def get_current_user(self,token):
        response=self.client.get(
            path=reverse("current-user"),
            headers={"Authorization": f"Bearer {token}"},
        )
        return response