from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(product)
admin.site.register(contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(Categorydetail)