from django.contrib import admin

# Register your models here.
from analytics.models import EodReport, PublisherSalesReport, BookSalesReport, LowInvReport


class EoDModelAdmin(admin.ModelAdmin):
    list_display = ["date"]
    list_filter = ["date"]


    class Meta:
        model = EodReport


class PublisherSalesModelAdmin(admin.ModelAdmin):
    list_display = ["date"]
    list_filter = ["date"]

    class Meta:
        model = PublisherSalesReport


class BookSalesModelAdmin(admin.ModelAdmin):
    list_display = ["date"]
    list_filter = ["date"]

    class Meta:
        model = BookSalesReport


class LowInventoryModelAdmin(admin.ModelAdmin):
    class Meta:
        model = LowInvReport


admin.site.register(EodReport, EoDModelAdmin)
admin.site.register(PublisherSalesReport, PublisherSalesModelAdmin)
admin.site.register(BookSalesReport, BookSalesModelAdmin)
admin.site.register(LowInvReport, LowInventoryModelAdmin)

