# Book Store

Book store semester project for CSCI 4050 - Summer 2018.

# Requirements:
RabbitMQ server: http://www.rabbitmq.com/install-windows.html

# Running celery:
$ celery -A bookstore worker --loglevel=info -P eventlet
