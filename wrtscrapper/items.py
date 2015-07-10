# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'wrtweb.settings'
from scrapy_djangoitem import DjangoItem

from wrtprices.models import Device, PriceOffer, PriceSummary, Brand
import django
django.setup()


class DeviceItem(DjangoItem):
    django_model = Device


class PriceOfferItem(DjangoItem):
    django_model = PriceOffer


class PriceSummaryItem(DjangoItem):
    django_model = PriceSummary
