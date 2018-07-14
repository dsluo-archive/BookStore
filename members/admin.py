from django.contrib import admin

# Register your models here.
from members.models import Member, Address


class AddressModelAdmin(admin.ModelAdmin):
    list_display = ["location", "member"]

    def member(self, obj):
        return obj

    class Meta:
        model = Member


class MemberModelAdmin(admin.ModelAdmin):
    list_display = ["user"]

    class Meta:
        model = Member


admin.site.register(Member, MemberModelAdmin)
admin.site.register(Address, AddressModelAdmin)

