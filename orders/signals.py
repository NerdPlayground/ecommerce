from .models import Order
from django.conf import settings
from django.dispatch import receiver,Signal
from django.db.models.signals import post_save

deliver_order=Signal()

def send_message(customer,content):
    try:
        response=settings.SMS.send(
            f"Hello {customer}, {content}",
            [customer.phone_number],settings.AT_SENDER
        )
        print("{0}{1}{0}".format("\n"+"="*50+"\n",response))
    except Exception as e:
        error=f"There seems to be a problem: {e}"
        print("{0}{1}{0}".format("\n"+"="*50+"\n",error))

@receiver(post_save,sender=Order)
def order_created_handler(sender,instance,created,**kwargs):
    if not created: return
    content="Your order has been received and it will be delivered soon. Thank you for shopping with us :)"
    send_message(instance.customer,content)

@receiver(deliver_order,sender=Order)
def order_delivered_handler(sender,instance,**kwargs):
    content="Your order has been processed and is on its way. Thank you for shopping with us :)"
    send_message(instance.customer,content)