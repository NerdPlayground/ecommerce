import random
from .models import Product
from django.urls import reverse
from pocket.tests import PocketTestCase

class ProductTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()
    
    def add_product(self,actor):
        token=self.member_login(actor)
        count=Product.objects.count()
        data={
            "name":"Cargo Pants",
            "price":2999,
        }
        response=self.client.post(
            path=reverse("add-product"),
            data=data,
            headers={"Authorization": f"Bearer {token}"},
        )
        return response,data,count

    def test_admin_add_product(self):
        response,data,count=self.add_product(self.admin)
        self.assertEqual(response.status_code,201)
        self.assertEqual(Product.objects.count(),count+1)

        product=Product.objects.first()
        self.assertEqual(product.name,data.get("name"))
        self.assertEqual(product.price,data.get("price"))
    
    def test_member_add_product(self):
        response,data,count=self.add_product(self.member)
        self.assertEqual(response.status_code,403)
        self.assertEqual(Product.objects.count(),count)
    
    def test_get_all_products(self):
        products_count=Product.objects.count()
        response=self.client.get(path=reverse("products"))
        self.assertEqual(response.status_code,200)
        self.assertEqual(products_count,len(response.json()))
    
    def test_get_product_with_id(self):
        product=random.choice(self.products)
        response=self.client.get(path=reverse(
            "product-detail",
            kwargs={"pk":product.id}
        ))
        self.assertEqual(response.status_code,200)
        
        retrieved=response.json()
        self.assertEqual(str(product.id),retrieved.get("id"))
    
    def update_product(self,actor):
        token=self.member_login(actor)
        product=random.choice(self.products)
        data={
            "name":"Cargo Pants",
            "price":2999,
        }
        response=self.client.put(
            path=reverse("modify-product",kwargs={"pk":product.id}),
            headers={"Authorization": f"Bearer {token}"},
            content_type="application/json",
            data=data,
        )
        return (response,data)
    
    def test_admin_update_product(self):
        response,data=self.update_product(self.admin)
        self.assertEqual(response.status_code,200)

        updated=response.json()
        self.assertEqual(updated.get("name"),data.get("name"))
        self.assertEqual(updated.get("price"),data.get("price"))
    
    def test_member_update_product(self):
        response,data=self.update_product(self.member)
        self.assertEqual(response.status_code,403)
    
    def delete_product(self,actor):
        products=Product.objects.count()
        product=random.choice(self.products)
        token=self.member_login(actor)
        response=self.client.delete(
            path=reverse("modify-product",kwargs={"pk":product.id}),
            headers={"Authorization": f"Bearer {token}"}
        )
        return response,products
    
    def test_admin_delete_product(self):
        response,products=self.delete_product(self.admin)
        self.assertEqual(response.status_code,204)
        self.assertEqual(Product.objects.count(),products-1)
    
    def test_member_delete_product(self):
        response,products=self.delete_product(self.member)
        self.assertEqual(response.status_code,403)
        self.assertEqual(Product.objects.count(),products)
