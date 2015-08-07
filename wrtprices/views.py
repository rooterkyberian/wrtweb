from django.shortcuts import render
from django.db.models import Count
from django_tables2 import RequestConfig

from wrtprices.models import Device
from wrtprices.tables import DeviceTable


def devices(request):
    devices_annotated = Device.objects\
        .annotate(price_info_null=Count('price_info'))
    table = DeviceTable(devices_annotated)
    RequestConfig(request).configure(table)
    return render(request, 'devices.html', {'table': table})
