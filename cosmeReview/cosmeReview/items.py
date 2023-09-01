# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class reviewItem(scrapy.Item):
    productId = scrapy.Field()
    productName = scrapy.Field()
    productUrl = scrapy.Field()
    productRating = scrapy.Field()
    productRanking = scrapy.Field()

    brandId = scrapy.Field()
    brandName = scrapy.Field()
    brandUrl = scrapy.Field()

    reviewId = scrapy.Field()
    reviewUrl = scrapy.Field()
    reviewRating = scrapy.Field()
    reviewText = scrapy.Field()

    userId = scrapy.Field()
    userName = scrapy.Field()
    userAge = scrapy.Field()
    userUrl = scrapy.Field()

