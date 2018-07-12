from bookstore.celery import app


@app.task
def cancel_reservation(member_slug, book_slug):

    from members.models import Member
    from books.models import Book

    member = Member.objects.all().filter(slug=member_slug).first()
    book = Book.objects.all().filter(slug=book_slug).first()

    return member.cart.cancel_purchase(member, book)
