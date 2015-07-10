from django.contrib import admin

from .models import Brand, Device, PriceSummary, PriceOffer


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'devices_count')


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'by', 'version', 'link', 'going_price')


class PriceSummaryAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'date', 'going_price')


class PriceOfferAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'link', 'date', 'price')


admin.site.register(Brand, BrandAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(PriceSummary, PriceSummaryAdmin)
admin.site.register(PriceOffer, PriceOfferAdmin)
