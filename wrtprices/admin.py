from django.contrib import admin

from .models import Brand, Device, PriceSummary, PriceOffer

admin.site.register(Brand)
admin.site.register(Device)
admin.site.register(PriceSummary)
admin.site.register(PriceOffer)
