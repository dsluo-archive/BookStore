from celery import Celery
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')

app = Celery('tasks')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def send_newsletter():
    from members.views import daily_newsletter
    from books.views import generate_promotion

    code = generate_promotion()
    daily_newsletter(code)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(86400, send_newsletter.s(), name='add 10 and 9')


if __name__ == '__main__':
    app.start()
