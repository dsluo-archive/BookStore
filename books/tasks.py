from books.models import PromotionCodes
from bookstore.celery import app


@app.task
def cancel_promotional(promotional_code):
    promotional = PromotionCodes.objects.all().filter(code=promotional_code).first()

    if promotional:
        promotional.delete()
        return True

    return False
