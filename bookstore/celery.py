import os

from celery import Celery
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
    delay = 60  # 86400
    sender.add_periodic_task(delay, send_newsletter.s(), name='daily_newsletter')


if __name__ == '__main__':
    app.start()
