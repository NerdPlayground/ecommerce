import re
from .models import Customer
from django.core import mail
from django.urls import reverse
from knox.models import AuthToken
from pocket.tests import PocketTestCase
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

class CustomerTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()
    
    def verify_user_email(self,username):
        pattern="key: (?P<key>[-:\w]+)"
        key=re.search(pattern,mail.outbox[0].body).group("key")
        response=self.client.post(reverse("rest_verify_email"),{"key":key})
        self.assertEqual(response.status_code,200)

        current_user=get_user_model().objects.get(username=username)
        email_address=EmailAddress.objects.get(user=current_user)
        self.assertTrue(email_address.verified)

    def setup_customer_details(self,token,username,email,details):
        response=self.client.put(
            headers={"Authorization": f"Bearer {token}"},
            path=reverse("current-user"),
            content_type="application/json",
            data={
                "username":username,"email":email,
                "first_name":details.get("first_name"),
                "last_name":details.get("last_name"),
                "customer":details.get("customer"),
            }
        )
        self.assertEqual(response.status_code,200)

    def test_member_registration(self):
        username="johndoe"
        email=f"{username}@gmail.com"
        response=self.client.post(reverse("rest_register"),{
            "username":username,
            "email":email,
            "password1":self.password,
            "password2":self.password,
        })
        self.assertEqual(response.status_code,204)
        self.assertEqual(len(mail.outbox),1)
        self.verify_user_email(username)

        customer=Customer.objects.last()
        token=self.member_login(customer,self.password)
        details={
            "first_name":"George",
            "last_name":"Mobisa",
            "customer":{"phone_number":"+254712345678"}
        }
        self.setup_customer_details(token,username,email,details)

        customer=Customer.objects.last()
        self.assertEqual(customer.user.username,username)
        self.assertEqual(customer.user.email,email)
        self.assertEqual(customer.user.first_name,details.get("first_name"))
        self.assertEqual(customer.user.last_name,details.get("last_name"))
        self.assertEqual(customer.phone_number,details.get("customer").get("phone_number"))
    
    def test_member_delete_account(self):
        token=self.member_login(self.dummy)
        total_members=Customer.objects.count()
        response=self.client.delete(
            path=reverse("current-user"),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,204)
        self.assertEqual(Customer.objects.count(),total_members-1)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,401)
    
    def test_member_change_password(self):
        token=self.member_login(self.member)
        password="QWERTY23!@#"
        response=self.client.post(
            headers={"Authorization": f"Bearer {token}"},
            path=reverse("rest_password_change"),
            data={
                "old_password":self.password,
                "new_password1":password,
                "new_password2":password,
            }
        )
        self.assertEqual(response.status_code,200)

        logout_response=self.client.post(
            path=reverse("knox_logout"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(logout_response.status_code,204)
        
        new_token=self.member_login(self.member,password)
        user_response=self.get_current_user(new_token)
        self.assertEqual(user_response.status_code,200)
    
    def test_member_password_reset(self):
        response=self.client.post(
            path=reverse("password_reset:reset-password-request"),
            data={"email":self.member.user.email},
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(mail.outbox),1)

        pattern="Authentication Token: (?P<token>[\w]+)"
        token=re.search(pattern,mail.outbox[0].body).group("token")
        token_response=self.client.post(
            path=reverse("password_reset:reset-password-validate"),
            data={"token":token}
        )
        self.assertEqual(token_response.status_code,200)

        password="QWERTY23!@#"
        reset_response=self.client.post(
            path=reverse("password_reset:reset-password-confirm"),
            data={"token":token,"password":password,}
        )
        self.assertEqual(reset_response.status_code,200)
        
        new_token=self.member_login(self.member,password)
        user_response=self.get_current_user(new_token)
        self.assertEqual(user_response.status_code,200)
    
    def test_member_logout(self):
        token_counter=AuthToken.objects.count()
        token=self.member_login(self.member)
        self.assertEqual(AuthToken.objects.count(),token_counter+1)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,200)

        response=self.client.post(
            path=reverse("knox_logout"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,204)
        self.assertEqual(AuthToken.objects.count(),token_counter)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,401)
    
    def test_member_logout_all_sessions(self):
        token_counter=AuthToken.objects.filter(user=self.member.user).count()
        all_tokens=AuthToken.objects.count()
        token=self.member_login(self.member)
        self.assertEqual(AuthToken.objects.count(),token_counter+1)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,200)

        response=self.client.post(
            path=reverse("knox_logout_all"),
            headers={"Authorization":f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,204)
        self.assertEqual(AuthToken.objects.count(),all_tokens-token_counter)

        user_response=self.get_current_user(token)
        self.assertEqual(user_response.status_code,401)
    
    def access_all_users(self,actor):
        token=self.member_login(actor)
        count=Customer.objects.count()
        response=self.client.get(
            path=reverse("user-list"),
            headers={"Authorization":f"Bearer {token}"},
        )
        return response,count

    def test_admin_access_all_users(self):
        response,count=self.access_all_users(self.admin)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json()),count)
    
    def test_member_access_all_users(self):
        response,count=self.access_all_users(self.member)
        self.assertEqual(response.status_code,403)
    
    def test_member_search_for_user(self):
        token=self.member_login(self.member)
        username=self.intruder.user.username
        response=self.client.get(
            path=reverse("user-detail",kwargs={"username":username}),
            headers={"Authorization":f"Bearer {token}"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(username,response.json().get("username"))
