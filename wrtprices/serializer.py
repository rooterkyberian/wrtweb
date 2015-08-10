from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from wrtprices.models import Brand, Device, PriceSummary


class PriceSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceSummary


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    brand_name = PrimaryKeyRelatedField(source='by',
                                        queryset=Brand.objects.all())
    price_info = PriceSummarySerializer()

    class Meta:
        model = Device
        fields = (
            "brand_name", "name", "version", "link",
            "status", "target", "platform",
            "cpu_speed", "flash", "ram",
            "wnic", "wireless", "wired", "usb",
            "other", "price_info"
        )
