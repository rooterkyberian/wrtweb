from django.shortcuts import render
from django_tables2 import RequestConfig

from wrtprices.models import Device
from wrtprices.tables import DeviceTable


def devices(request):
    table = DeviceTable(Device.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'devices.html', {'table': table})
