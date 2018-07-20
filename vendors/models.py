import random
import string

from django.db import models
from django.db.models.signals import pre_save

# Create your models here.


def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=60, unique=True)
    vendor_passcode = models.CharField(max_length=16, default=generate_code, blank=True)

    def __str__(self):
        return self.vendor_name

