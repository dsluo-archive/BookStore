from django.contrib import admin

# Register your models here.
from members.models import Member


class MemberModelAdmin(admin.ModelAdmin):
    list_display = ["user"]

    class Meta:
        model = Member


admin.site.register(Member, MemberModelAdmin)
