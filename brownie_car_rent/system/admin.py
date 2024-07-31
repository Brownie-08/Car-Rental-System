from django.contrib import admin
from .models import Car, Order, PrivateMsg
# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ("car_name", "image", "company_name")
class OrderAdmin(admin.ModelAdmin):
    list_display = ("car_name", "date_from", "date_to", "dealer_name",)

class PrivateMsgAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message")

admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PrivateMsg, PrivateMsgAdmin)