from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

class Device(models.Model):
    name = models.CharField(max_length=255)
    by = models.ForeignKey(Brand)
    version = models.CharField(max_length=255, null=True)
    link = models.URLField()

    status = models.CharField(max_length=255)
    target = models.CharField(max_length=60)
    platform = models.CharField(max_length=255)

    cpu_speed = models.CharField(max_length=255)
    flash = models.CharField(max_length=60)
    ram = models.CharField(max_length=60)

    wnic = models.CharField(max_length=255)
    wireless = models.CharField(max_length=255)
    wired = models.CharField(max_length=255)
    usb = models.CharField(max_length=60)

    other = models.TextField()



class PriceSummary(models.Model):
    device = models.ForeignKey(Device)
    going_price = models.FloatField(min_value=0.0)
    invalidated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


class PriceOffer(models.Model):
    summary = models.ForeignKey(PriceSummary)
    device = models.ForeignKey(Device)
    price = models.FloatField(min_value=0.0)
    price_with_shipping = models.FloatField(min_value=0.0, null=True)
    date = models.DateTimeField(auto_now_add=True)