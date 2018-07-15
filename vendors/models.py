from django.db import models


# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=60)

    def __str__(self):
        return self.vendor_name
