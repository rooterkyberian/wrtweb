# Scrapy settings for wrtscrapper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'wrtscrapper'

SPIDER_MODULES = ['wrtscrapper.spiders']
NEWSPIDER_MODULE = 'wrtscrapper.spiders'

DOWNLOAD_DELAY = 2
REDIRECT_MAX_TIMES = 8

ITEM_PIPELINES = {"wrtscrapper.pipelines.WrtscrapperPipeline": 800}
