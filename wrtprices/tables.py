# -*- coding: UTF-8 -*-

# Copyright (c) 2015 Maciej Urbański <rooter@kyberian.net>

import django_tables2 as tables
from wrtprices.models import Device


class DeviceTable(tables.Table):
    going_price = tables.Column(orderable=False)

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
