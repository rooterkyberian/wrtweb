from django.shortcuts import render
from django.db.models import Count
from django_tables2 import RequestConfig
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import pagination

from wrtprices.models import Device, PriceSummary
from wrtprices.serializer import PriceSummarySerializer, DeviceSerializer
from wrtprices.tables import DeviceTable


def devices(request):
    devices_annotated = Device.objects\
        .annotate(price_info_null=Count('price_info'))
    table = DeviceTable(devices_annotated)
    RequestConfig(request).configure(table)
    return render(request, 'devices.html', {'table': table})


class PriceSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceSummary.objects.all()
    serializer_class = PriceSummarySerializer
    pagination_class = pagination.PageNumberPagination
    paginate_by = 10


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    pagination_class = pagination.PageNumberPagination
    paginate_by = 10
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ('by__name', 'name')
    ordering_fields = '__all__'
