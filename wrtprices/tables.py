# -*- coding: UTF-8 -*-

# Copyright (c) 2015 Maciej Urbański <rooter@kyberian.net>

import django_tables2 as tables
from django_tables2.utils import OrderBy, OrderByTuple
from wrtprices.models import Device


class OrderByRestricted(OrderBy):
    """
    Restrict opposite sort influence of OrderBy.
    """
    @property
    def opposite(self):
        """
        Return an `.OrderBy` object with not opposite sort influence.

        Example:

        .. code-block:: python

            >>> order_by = OrderBy('name')
            >>> order_by.opposite
            'name'

        :rtype: `.OrderBy` object
        """
        return OrderByRestricted(self)


class DeviceTable(tables.Table):
    going_price = tables.Column(
        order_by="price_info.going_price"
    )
    going_price.order_by = OrderByTuple(
        (OrderByRestricted("-price_info_null"),) + going_price.order_by
    )

    class Meta:
        model = Device
        fields = (
            "by", "name", "version", "link",
            "status", "target", "platform",
            "cpu_speed", "flash", "ram",
            "wnic", "wireless", "wired", "usb",
            "other", "going_price"
        )
        order_by = ("by", "name", "version")

        # add class="paleblue" to <table> tag
        attrs = {"class": "paleblue"}
