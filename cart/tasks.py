from bookstore.celery import app
from cart.models import Order

@app.task
def cancel_reservation(order_id):
    order = Order.objects.all().filter(confirmation_number=order_id).first()

    if order and not order.is_fulfilled:
        return order.cancel_order()
