# -*- coding: UTF-8 -*-

# Copyright (c) 2015 Maciej Urbański <rooter@kyberian.net>

import urlparse
import re

from scrapy.spiders import Spider
from scrapy.http import FormRequest

import wrtscrapper.items


def median(l):
    m, r = divmod(len(l), 2)
    if r:
        return sorted(l)[m]
    return sum(sorted(l)[m - 1:m + 1]) / 2


class AllegroAuc(Spider):
    name = "allegro"
    allowed_domains = ["allegro.pl"]
    # http://allegro.pl/listing/listing.php?order=qd&string=wdr3600&offerTypeBuyNow=1
    start_urls = ["http://allegro.pl/komputery", ]

    PRICE_REGEXP = re.compile(r'[^\d]*([\d\s]+(,\d{1,2})?)\s+')

    def device_queries(self):
        for device in wrtscrapper.items.Device.objects.all():
            keywords = str(device)

            yield device, keywords

    def form_next_request(self, response):
        """
        :type response: scrapy.http.Response
        """

        req = None
        gen = response.meta["device_keywords_generator"]
        try:
            device, keywords = gen.next()
            req = FormRequest.from_response(response,
                                            formdata={'string': keywords},
                                            callback=self.parse_search_page)
            req.meta["auc_item"] = device
            req.meta["device_keywords_generator"] = \
                response.meta["device_keywords_generator"]
            req.dont_filter = True
        except StopIteration:
            pass

        return req

    def parse(self, response):
        """
        :type response: scrapy.http.Response
        """

        gen = self.device_queries()
        response.meta["device_keywords_generator"] = gen

        yield self.form_next_request(response)

    @staticmethod
    def extract_first_and_strip(selector):
        if len(selector) > 0:
            return selector[0].extract().strip()
        return None

    @staticmethod
    def price_to_float(selector):
        text = ''.join(selector.extract()).strip()
        match = re.match(AllegroAuc.PRICE_REGEXP, text)

        if match is None:
            raise ValueError("""Price tag not found in string '%s'.""" % text)

        price_tag = match.group(1)
        price_tag = price_tag.replace(' ', '').replace(',', '.', 1)
        return float(price_tag)

    def parse_search_page(self, response):
        """
        :type response: scrapy.http.Response
        """

        device = response.meta["auc_item"]

        auc_sum = wrtscrapper.items.PriceSummaryItem()
        auc_sum["device"] = device

        prices = []
        auction_objs = []

        auctions = response.xpath("""//article[contains(@class,'offer')]""")
        for auction in auctions:
            try:
                item = wrtscrapper.items.PriceOfferItem()
                item["device"] = device
                item['link'] = urlparse.urljoin(
                    response.url,
                    AllegroAuc.extract_first_and_strip(
                        auction.xpath(".//h2/a/@href"))
                )
                item['price'] = AllegroAuc.price_to_float(
                    auction.xpath(
                        ".//div["
                        "contains(@class,'offer-price') or"
                        "contains(@class,'price')"
                        "]//text()"
                    )
                )
                prices.append(item['price'])

                try:
                    delivery_price_selector = auction.xpath(
                        ".//span[contains(@class,'offer-delivery')]//text()"
                    )

                    item['price_with_shipping'] = AllegroAuc.price_to_float(
                        delivery_price_selector
                    )
                except ValueError:
                    self.logger.debug("No shipping price")

                auction_objs.append(item.instance)
                yield item
            except ValueError:
                import traceback
                self.logger.debug(traceback.format_exc())
                self.logger.warning(
                    'Exception raised during parsing of %s at %s'
                    % (auction.extract(), response.url)
                )

        auc_sum["offers_count"] = len(prices)
        if auc_sum["offers_count"] > 0:
            auc_sum["going_price"] = median(prices)
            auc_sum.save()
            map(auc_sum.instance.offers.add, auction_objs)
            yield auc_sum

        yield self.form_next_request(response)
        yield self.form_next_request(response)
