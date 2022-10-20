from django.contrib import admin

from buyer.models import Donation, User,Blog


# Register your models here.
admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Donation)


