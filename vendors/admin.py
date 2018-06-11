from django.contrib import admin

# Register your models here.
from vendors.models import Vendor


class VendorModelAdmin(admin.ModelAdmin):
    list_display = ["vendor_name"]

    class Meta:
        model = Vendor

admin.site.register(Vendor, VendorModelAdmin)
