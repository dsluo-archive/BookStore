from django.contrib import admin

# Register your models here.
from client.models import Client


class ClientModelAdmin(admin.ModelAdmin):
    list_display = ["member"]

    class Meta:
        model = Client

admin.site.register(Client, ClientModelAdmin)
