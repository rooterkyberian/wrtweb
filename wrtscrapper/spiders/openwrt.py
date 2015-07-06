# -*- coding: UTF-8 -*-

# Copyright (c) 2015 Maciej Urbański <rooter@kyberian.net>

from itertools import izip

from scrapy.spiders import Spider

from wrtscrapper.items import DeviceItem


class OpenwrtTOH(Spider):
    name = "openwrt_toh"
    allowed_domains = ["openwrt.org"]
    start_urls = [
        "http://wiki.openwrt.org/toh/start",
    ]

    def parse(self, response):

        toh = response.xpath("//div[h1/text()='Table of Hardware']")

        title_n_table_selectors = toh.xpath(
            "h2 | h3 | div[@class='level3']//table")

        brand = "Unknown"
        support_group = "X"
        name_map = {"Model": "name",
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

        for selector in title_n_table_selectors:
            h2_text = selector.xpath("self::h2//text()")
            h3_text = selector.xpath("self::h3//text()")
            if len(h2_text) > 0:
                support_group = "".join(h2_text.extract())
            elif len(h3_text) > 0:
                brand = "".join(h3_text.extract())
            elif len(selector.xpath("self::table")) > 0:
                header = []
                table_selector = selector
                for ths in table_selector.xpath(".//th"):
                    field_name = "".join(ths.xpath(".//text()").extract())
                    header.append(field_name.strip())

                for trs in table_selector.xpath(
                        ".//tr/following-sibling::tr"):
                    hw_dict = {"by": brand, "other": ""}
                    for field_name, tds in izip(header, trs.xpath(".//td")):
                        value = "".join(tds.xpath(".//text()").extract())
                        value = value.strip()
                        if field_name == "Model":
                            hw_dict["link"] = " ".join(
                                tds.xpath(".//a/@href").extract())

                        if field_name in name_map:
                            hw_dict[name_map[field_name]] = value
                        else:
                            hw_dict["other"] += "%s = %s; " % (
                                field_name, value)
                    if "name" in hw_dict:
                        yield DeviceItem(hw_dict)
