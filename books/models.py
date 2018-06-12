from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.db.models.signals import pre_save

# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" % (instance.slug, filename)


class Book(models.Model):

    id = models.AutoField(primary_key=True)

    item_picture = models.ImageField(upload_to=upload_location, null=True, blank=True)

    name = models.CharField(max_length=120)
    isbn = models.CharField(max_length=30)
    publisher = models.CharField(max_length=60)
    author = models.CharField(max_length=60)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    publish_date = models.DateField()

    count_in_stock = models.IntegerField(default=1, blank=True)

    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()

    def get_absolute_url(self):
        return reverse("books:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Reservation(models.Model):
    book = models.OneToOneField(Book, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)


def create_slug(instance):
    current_id = Book.objects.all().order_by("-id").first()
    if current_id:
        current_id = current_id.id
    else:
        current_id = 1

    return slugify(instance.name) + "-" + str(current_id)


def pre_save_item_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_item_receiver, sender=Book)