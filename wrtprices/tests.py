from django.db import IntegrityError
from django.test import TestCase

from wrtprices.models import Brand, Device, PriceOffer, PriceSummary


class BrandTestCase(TestCase):
    BRANDS = ["Linksys", "TP-Link"]

    def setUp(self):
        """
        Set up test cases.
        """
        Brand.objects.create(name="Linksys")
        Brand.objects.create(name="TP-Link")

    def test_all(self):
        self.assertSetEqual(set(BrandTestCase.BRANDS),
                            set([brand.name for brand in Brand.objects.all()]))

    def test_unique(self):
        brand = Brand.objects.first()
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name=brand.name)


class PriceOfferTestCase(TestCase):
    def setUp(self):
        """
        Set up test cases.
        """
        PriceOffer.objects.create()


class DeviceTestCase(TestCase):
    def setUp(self):
        """
        Set up test cases.
        """
        Device.objects.create(name="WRT54G")
        Device.objects.create(name="WRT54GL")

    def test_hash(self):
        devices = Device.objects.all()
        hashes = set([device.hash for device in devices])
        self.assertGreater(len(hashes), 0)
        self.assertEqual(len(devices), len(hashes))

    def test_unique(self):
        device = Device.objects.first()
        with self.assertRaises(IntegrityError):
            Device.objects.create(name=device.name, by=device.by,
                                  version=device.version)

    def test_unique(self):
        device = Device.objects.first()

        with self.assertRaises(IntegrityError):
            Device.objects.create(name=device.name, by=device.by,
                                  version=device.version)

    def test_unique_modified(self):
        device = Device.objects.first()
        if device.version is None:
            device.version = 'v1'
        device.version += '.2'
        device.save()

        with self.assertRaises(IntegrityError):
            Device.objects.create(name=device.name,
                                  by=device.by,
                                  version=device.version)

