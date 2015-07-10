import wrtscrapper.items
from scrapy_djangoitem import DjangoItem


class WrtscrapperPipeline(object):
    def process_item(self, item, spider):
        if issubclass(type(item), DjangoItem):
            item.save()
        return item
