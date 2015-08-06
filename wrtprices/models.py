import datetime
import random
import hashlib

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import django.utils.encoding


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


class HashedModel(models.Model):
    HASH_HEXLEN = 40
    hash = models.CharField(max_length=HASH_HEXLEN, primary_key=True)

    def _generate_hash(self):
        hashed = '%030x' % random.randrange(16 ** HashedModel.HASH_HEXLEN)
        return hashed

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = self._generate_hash()
        return super(HashedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


@django.utils.encoding.python_2_unicode_compatible
class Brand(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.name

    def devices_count(self):
        return Device.objects.filter(by=self).count()


@django.utils.encoding.python_2_unicode_compatible
class Device(HashedModel):
    name = models.CharField(max_length=255)
    by = models.ForeignKey(Brand, null=True)
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

    def _generate_hash(self):
        hashed = hashlib.sha1()
        if self.by:
            hashed.update(self.by.name)
        for o in self.name, self.version:
            hashed.update(str(o))
        return hashed.hexdigest()

    def __str__(self):
        return self.fullname()

    def fullname(self):
        ret = ""
        if self.by:
            ret = self.by.name + " "
        ret += self.name
        if self.version:
            ret += " " + self.version
        return ret

    def going_price(self):
        price_summary = PriceSummary.objects.filter(
            device=self,
            invalidated=False,
        ).latest(field_name='date')

        if price_summary:
            return price_summary.going_price

        return None


@django.utils.encoding.python_2_unicode_compatible
class PriceOffer(HashedModel):
    link = models.URLField()
    device = models.ForeignKey(Device)
    price = MinMaxFloat(min_value=0.0)
    price_with_shipping = MinMaxFloat(min_value=0.0, null=True)
    date = models.DateTimeField()

    def _generate_hash(self):
        hashed = hashlib.sha1()
        for o in self.link, self.date:
            hashed.update(str(o))
        return hashed.hexdigest()

    def device_name(self):
        return self.device.fullname()

    def __str__(self):
        return "%s @ %s" % (self.link, self.date)

    def save(self, *args, **kwargs):
        """ set date if none specified """
        if not self.date:
            self.date = datetime.datetime.today()
        return super(PriceOffer, self).save(*args, **kwargs)


@django.utils.encoding.python_2_unicode_compatible
class PriceSummary(models.Model):
    device = models.ForeignKey(Device)
    going_price = MinMaxFloat(min_value=0.0, null=True)
    invalidated = models.BooleanField(default=False)
    offers_count = models.IntegerField(default=0)
    validated_offers_count = models.IntegerField(default=0)
    date = models.DateTimeField()
    offers = models.ManyToManyField(PriceOffer)

    def device_name(self):
        return self.device.fullname()

    def __str__(self):
        return "%s @ %s" % (self.device.name, self.date)

    def save(self, *args, **kwargs):
        """ set date if none specified """
        if not self.date:
            self.date = datetime.datetime.today()
        return super(PriceOffer, self).save(*args, **kwargs)
