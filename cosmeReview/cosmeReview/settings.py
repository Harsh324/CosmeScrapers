
BOT_NAME = "cosmeReview"

SPIDER_MODULES = ["cosmeReview.spiders"]
NEWSPIDER_MODULE = "cosmeReview.spiders"

# LOG_LEVEL = 'WARNING'
LOG_FILE = 'error.log'

ROBOTSTXT_OBEY = False

HTTP_PROXY = 'http://127.0.0.1:8118'
# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'
# DEFAULT_REQUEST_HEADERS = {}
CONCURRENT_REQUESTS = 8

DOWNLOADER_MIDDLEWARES = {
	'cosmeReview.middlewares.ProxyMiddleware': 543,
	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "cosmeReview.pipelines.CosmeReviewPipeline": 300,
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
