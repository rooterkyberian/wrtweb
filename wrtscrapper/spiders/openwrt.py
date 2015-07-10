# -*- coding: UTF-8 -*-

# Copyright (c) 2015 Maciej Urbański <rooter@kyberian.net>

from itertools import izip

from scrapy.spiders import Spider

import wrtscrapper.items


class OpenwrtTOH(Spider):
    name = "openwrt_toh"
    allowed_domains = ["openwrt.org"]
    start_urls = [
        "http://wiki.openwrt.org/toh/start",
    ]

    name_map = {
        "Model": "name",
        "Version": "version",
        "Status": "status",
        "Target(s)": "target",
        "Platform": "platform",
        "CPU Speed (MHz)": "cpu_speed",
        "Flash (MB)": "flash",
        "RAM (MB)": "ram",
        "Wireless NIC": "wnic",
        "Wireless Standard": "wireless",
        "Wired Ports": "wired",
        "USB": "usb",
    }

    def parse(self, response):

        toh = response.xpath("//div[h1/text()='Table of Hardware']")

        title_n_table_selectors = toh.xpath(
            "h2 | h3 | div[@class='level3']//table")

        brand = "Unknown"
        support_group = "X"

        for selector in title_n_table_selectors:
            h2_text = selector.xpath("self::h2//text()")
            h3_text = selector.xpath("self::h3//text()")
            if len(h2_text) > 0:
                support_group = "".join(h2_text.extract())
            elif len(h3_text) > 0:
                brand = "".join(h3_text.extract()).strip()
                if "unbranded" in brand.lower():
                    brand_object = None
                else:
                    brand_object, _created = wrtscrapper.items. \
                        Brand.objects.get_or_create(name=brand)
            else:
                for table_selector in selector.xpath("self::table"):
                    for item in self.parse_table(table_selector):
                        yield item

    def parse_table(self, table_selector, brand_object):
        header = []
        for ths in table_selector.xpath(".//th"):
            field_name = "".join(ths.xpath(".//text()").extract())
            header.append(field_name.strip())

        for trs in table_selector.xpath(".//tr[td]"):
            hw_dict = {
                "by": brand_object,
                "other": ""
            }
            for field_name, tds in izip(header,
                                        trs.xpath(".//td")):
                value = "".join(tds.xpath(".//text()").extract())
                value = value.strip()

                if field_name == "Model":
                    hw_dict["link"] = " ".join(
                        tds.xpath(".//a/@href").extract())

                if not value:
                    continue

                if field_name in OpenwrtTOH.name_map:
                    hw_dict[OpenwrtTOH.name_map[field_name]] = value
                else:
                    hw_dict["other"] += "%s = %s; " % (
                        field_name, value)

            if "name" in hw_dict:
                if hw_dict.get("version", "").lower() in ("", "-", "?", "ALL"):
                    hw_dict.pop("version", None)

                yield wrtscrapper.items.DeviceItem(hw_dict)
