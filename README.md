# Book Store

Book store semester project for CSCI 4050 - Summer 2018.

# Requirements:
Django 2.0.6
Pillow 5.1.0
pytz 2018.4
celery 4.2.0
django-celery-beat 1.1.1
eventlet 0.23.0
RabbitMQ server: http://www.rabbitmq.com/install-windows.html

# Running celery:
$ celery -A bookstore worker --loglevel=info -P eventlet
