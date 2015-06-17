from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MinMaxFloat(models.FloatField):
    def __init__(self, min_value=None, max_value=None, *args, **kwargs):
        self.form_defaults = {}
        validators = kwargs.pop("validators", [])

        if min_value:
            self.min_value = min_value
            self.form_defaults["min_value"] = min_value
            validators.append(MinValueValidator(min_value))

        if max_value:
            self.max_value = max_value
            self.form_defaults["max_value"] = max_value
            validators.append(MaxValueValidator(max_value))

        kwargs["validators"] = validators
        super(MinMaxFloat, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        form_kwargs = dict(self.form_defaults)
        form_kwargs.update(kwargs)
        return super(MinMaxFloat, self).formfield(**form_kwargs)


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
    going_price = MinMaxFloat(min_value=0.0)
    invalidated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


class PriceOffer(models.Model):
    summary = models.ForeignKey(PriceSummary)
    device = models.ForeignKey(Device)
    price = MinMaxFloat(min_value=0.0)
    price_with_shipping = MinMaxFloat(min_value=0.0, null=True)
    date = models.DateTimeField(auto_now_add=True)
