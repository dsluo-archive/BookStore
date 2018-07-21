# Book Store

Book store semester project for CSCI 4050 - Summer 2018.

# Requirements:
RabbitMQ server: http://www.rabbitmq.com/install-windows.html  
requirements.txt

# Running celery:  
## For any asynchronous event:
$ celery -A bookstore worker --loglevel=info -P eventlet  
## For periodic events (newsletter):
In a separate terminal -> $ celery -A bookstore beat --loglevel=info
