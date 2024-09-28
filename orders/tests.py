import random
from .models import Order
from django.urls import reverse
from pocket.tests import PocketTestCase
from pocket.signals import CatchSignal
from django.db.models.signals import post_save
from .signals import deliver_order,order_created_handler,order_delivered_handler

class OrderTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        return super().setUpTestData()
    
    def setUp(self):
        post_save.disconnect(order_created_handler,sender=Order)
        deliver_order.disconnect(order_delivered_handler,sender=Order)
        return super().setUp()

    def tearDown(self):
        post_save.connect(order_created_handler,sender=Order)
        deliver_order.connect(order_delivered_handler,sender=Order)
        return super().tearDown()
    
    def test_member_make_order(self):
        token=self.member_login(self.member)
        count=Order.objects.count()
        data={"products":[product.id for product in self.products[:5]]}

        with CatchSignal(post_save) as handler:
            response=self.client.post(
                path=reverse("orders"),
                headers={"Authorization": f"Bearer {token}"},
                data=data,
            )
            self.assertEqual(response.status_code,201)
            self.assertEqual(Order.objects.count(),count+1)

        created=Order.objects.first()
        handler.assert_called_once_with(
            sender=Order,signal=post_save,
            instance=created,created=True,
            update_fields=None,raw=False,
            using='default'
        )

        self.assertEqual(created.customer,self.member)
        self.assertEqual(created.delivered,False)
        for product in created.products.all():
            self.assertTrue(product.id in data.get("products"))
    
    def get_all_orders(self,actor):
        token=self.member_login(actor)
        response=self.client.get(
            path=reverse("all-orders"),
            headers={"Authorization": f"Bearer {token}"},
        )
        return response
    
    def test_admin_get_all_orders(self):
        count=Order.objects.count()
        response=self.get_all_orders(self.admin)
        self.assertEqual(response.status_code,200)
        self.assertEqual(count,len(response.json()))
    
    def test_member_get_all_orders(self):
        response=self.get_all_orders(self.member)
        self.assertEqual(response.status_code,403)

    def test_member_get_orders(self):
        token=self.member_login(self.member)
        count=Order.objects.filter(customer=self.member).count()
        response=self.client.get(
            path=reverse("orders"),
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(count,len(response.json()))
    
    def get_order_by_id(self,actor):
        token=self.member_login(actor)
        order=random.choice(self.orders)
        response=self.client.get(
            path=reverse("order-detail",kwargs={"pk":order.id}),
            headers={"Authorization": f"Bearer {token}"},
        )
        return response,order
    
    def test_member_get_order_by_id(self):
        response,order=self.get_order_by_id(self.member)
        self.assertEqual(response.status_code,200)
        retrieved=response.json()
        self.assertEqual(str(order.id),retrieved.get("id"))
    
    def test_intruder_get_order_by_id(self):
        response,order=self.get_order_by_id(self.intruder)
        self.assertEqual(response.status_code,403)
    
    def update_order(self,actor):
        token=self.member_login(actor)
        order=random.choice(self.orders)
        data={"products":[product.id for product in self.products[5:]]}
        response=self.client.put(
            path=reverse("order-detail",kwargs={"pk":order.id}),
            headers={"Authorization": f"Bearer {token}"},
            content_type="application/json",
            data=data,
        )
        return response,data,order
    
    def test_member_update_order(self):
        response,data,order=self.update_order(self.member)
        self.assertEqual(response.status_code,200)

        order.refresh_from_db()
        self.assertEqual(order.customer,self.member)
        for product in order.products.all():
            self.assertTrue(product.id in data.get("products"))
    
    def test_intruder_update_order(self):
        response,data,order=self.update_order(self.intruder)
        self.assertEqual(response.status_code,403)
    
    def delete_order(self,actor):
        token=self.member_login(actor)
        order=random.choice(self.orders)
        count=Order.objects.count()
        response=self.client.delete(
            path=reverse("order-detail",kwargs={"pk":order.id}),
            headers={"Authorization": f"Bearer {token}"},
        )
        return response,count
    
    def test_member_delete_order(self):
        response,count=self.delete_order(self.member)
        self.assertEqual(response.status_code,204)
        self.assertEqual(Order.objects.count(),count-1)
    
    def test_intruder_delete_order(self):
        response,count=self.delete_order(self.intruder)
        self.assertEqual(response.status_code,403)
        self.assertEqual(Order.objects.count(),count)
    
    def deliver_order(self,actor):
        token=self.member_login(actor)
        order=random.choice(self.orders)
        with CatchSignal(deliver_order) as handler:
            response=self.client.put(
                path=reverse("deliver-order",kwargs={"pk":order.id}),
                headers={"Authorization": f"Bearer {token}"},
                content_type="application/json",
                data={"delivered":True},
            )
        return response,order,handler
    
    def test_admin_deliver_order(self):
        response,order,handler=self.deliver_order(self.admin)
        self.assertEqual(response.status_code,200)
        
        order.refresh_from_db()
        self.assertTrue(order.delivered)
        handler.assert_called_once_with(
            sender=Order,
            instance=order,
            signal=deliver_order,
        )
    
    def test_member_deliver_order(self):
        response,order,handler=self.deliver_order(self.member)
        self.assertEqual(response.status_code,403)
