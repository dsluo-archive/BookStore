from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
from vendors.models import Vendor


def upload_location(instance, filename):
    return "%s/%s/%s" % ("books", instance.slug, filename)


class Genre(models.Model):
    subjects = models.CharField(max_length=30)

    def __str__(self):
        return self.subjects


class Publisher(models.Model):
    name = models.CharField(max_length=120, unique=True, null=True, blank=False)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PromotionCodes(models.Model):
    code = models.CharField(max_length=6, unique=True, blank=False)
    genres = models.ManyToManyField(Genre, blank=True)
    discount = models.DecimalField(max_digits=2, decimal_places=2)


class Book(models.Model):
    item_picture = models.ImageField(upload_to=upload_location,
                                     default="books/images/default_book.png",
                                     null=True,
                                     blank=True)
    name = models.CharField(max_length=120)
    __original_name = None
    isbn = models.CharField(unique=True, max_length=30)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=False)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=False)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    publish_date = models.DateField()

    count_in_stock = models.IntegerField(default=1, blank=True)

    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()

    subjects = models.ManyToManyField(Genre)

    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=False)

    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("books:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        super(Book, self).__init__(*args, **kwargs)
        self.__original_name = self.name

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.name != self.__original_name:
            self.slug = create_slug(self)

        super(Book, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_name = self.name


def create_slug(instance):
    current_id = Book.objects.all().order_by("-id").first()

    if current_id:
        current_id = current_id.id

        while Book.objects.filter(slug=slugify(instance.name) + "-" + str(current_id)).exists():
            current_id += 1
    else:
        current_id = 1

    return slugify(instance.name) + "-" + str(current_id)


def post_save_item_receiver(sender, instance, created, **kwargs):

    from analytics.models import update_low_inventory
    update_low_inventory(instance, True)

post_save.connect(post_save_item_receiver, sender=Book)
