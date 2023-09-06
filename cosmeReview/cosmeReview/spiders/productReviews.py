import scrapy
from ..utils import LinkDetails, textHandler
from ..items import reviewItem

class cosmeSpider(scrapy.Spider):

    name = 'review'
    allowed_domains = ['www.cosme.net']
    

    def start_requests(self):
        urls = [
            'https://www.cosme.net/categories/item/802/ranking/',
        ]

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_product,
            )


    def parse_product(self, response):
        product_divs = response.css("div.keyword-ranking-item dl.clearfix")
  
        for product_div in product_divs:

            product_name = product_div.css("dd.summary h4.item a::text").get()
            product_name = textHandler()._filter_text(product_name)

            product_url = product_div.css("dd.summary h4.item a::attr(href)").get()
            product_id = None
            if product_url:
                product_id = LinkDetails(product_url).get_product_id()
                

            product_rating = product_div.css("dd.summary div.rating-point p.rating span::text").get()
            product_rating = textHandler()._filter_text(product_rating)


            product_ranking = product_div.css("dt span.rank-num span.num::text").get()
            product_ranking = textHandler()._filter_text(product_ranking)
            if not product_ranking:
                product_ranking = product_div.css("dt span.rank-num img::attr(alt)").get()

            brand_name = product_div.css("dd.summary div.clearfix span.brand a::text").get()
            brand_name = textHandler()._filter_text(brand_name)

            brand_url = product_div.css("dd.summary div.clearfix span.brand a::attr(href)").get()
            brand_id = None
            if brand_url:
                brand_id = LinkDetails(brand_url).get_brand_id()

            review_page_url = None
            if product_id:
                review_page_url = f"https://www.cosme.net/products/{product_id}/review/"

            
            yield scrapy.Request(
                url=review_page_url, 
                callback=self.parse_reviews,
                meta= {
                    "product_data" : {
                        "product_name": product_name,
                        "product_url": product_url,
                        "product_id": product_id,
                        "product_rating": product_rating,
                        "product_ranking" : product_ranking,
                        "brand_name": brand_name,
                        "brand_url": brand_url,
                        "brand_id": brand_id,
                    }
                }
            )
            

    def parse_reviews(self, response):
        review_divs = response.css("div.review-sec div.inner")

        for review_div in review_divs:
            user_url = review_div.css("div.head div.reviewer-info a::attr(href)").get()
            user_id = None
            if user_url:
                user_id = LinkDetails(user_url).get_user_id()
                

            user_name = review_div.css("div.head div.reviewer-info span.reviewer-name::text").get()
            user_name = textHandler()._filter_text(user_name)

            user_age = review_div.css("div.head div.reviewer-info ul")
            if user_age:
                user_age = user_age[0].css("li::text")
                if user_age:
                    user_age = user_age[0].get()
                    user_age = textHandler()._filter_text(user_age)


            review_rating = review_div.css("div.body div.rating p.reviewer-rating::text").get()
            review_rating = textHandler()._filter_text(review_rating)


            review_text = review_div.css("div.body p.read::text").getall()
            review_text = textHandler()._filter_text(review_text)

            review_id = None
            review_url = None
            review_link = review_div.css("div.body p.read span.read-more a::attr(href)").get()
            if review_link:
                review_id = LinkDetails(review_link).get_review_id()
                if review_id:
                    review_url = f"https://www.cosme.net/reviews/{review_id}/"


            if review_text:
                if review_text.endswith('\u2026'):
                    yield scrapy.Request(
                        url=review_url,
                        callback=self.parse_review,
                        meta={
                            "product_data" : response.meta['product_data'],
                            "review_data" : {
                                "review_id" : review_id,
                                "review_url" : review_url,
                                "review_rating" : review_rating,
                            },
                            "user_data" : {
                                "user_name" : user_name,
                                "user_id" : user_id,
                                "user_age" : user_age,
                                "user_url" : user_url
                            }
                        }
                    )
                else:
                    product_data = response.request.meta["product_data"]

                    item = reviewItem()
                    item['productId'] = product_data['product_id']
                    item['productName'] = product_data['product_name']
                    item['productUrl'] = product_data['product_url']
                    item['productRating'] = product_data['product_rating']
                    item['productRanking'] = product_data['product_ranking']

                    item['brandId'] = product_data['brand_id']
                    item['brandName'] = product_data['brand_name']
                    item['brandUrl'] = product_data['brand_url']

                    item['reviewId'] = review_id
                    item['reviewUrl'] = review_url
                    item['reviewRating'] = review_rating
                    item['reviewText'] = review_text

                    item['userId'] = user_id
                    item['userName'] = user_name
                    item['userAge'] = user_age
                    item['userUrl'] = user_url

                    yield item


        next_page_url = response.css("div.cmn-paging ul.clearfix li.next a::attr(href)").get()
        if next_page_url:
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse_reviews,
                meta={
                    "product_data": response.request.meta["product_data"]
                }
            )



    def parse_review(self, response):
        review_text = response.css("div.review-sec div.body p.read::text").getall()
        review_text = textHandler()._filter_text(review_text)

        product_data = response.request.meta["product_data"]
        review_data = response.request.meta["review_data"]
        user_data = response.request.meta["user_data"]

        item = reviewItem()
        item['productId'] = product_data['product_id']
        item['productName'] = product_data['product_name']
        item['productUrl'] = product_data['product_url']
        item['productRating'] = product_data['product_rating']
        item['productRanking'] = product_data['product_ranking']

        item['brandId'] = product_data['brand_id']
        item['brandName'] = product_data['brand_name']
        item['brandUrl'] = product_data['brand_url']

        item['reviewId'] = review_data['review_id']
        item['reviewUrl'] = review_data['review_url']
        item['reviewRating'] = review_data['review_rating']
        item['reviewText'] = review_text

        item['userId'] = user_data['user_id']
        item['userName'] = user_data['user_name']
        item['userAge'] = user_data['user_age']
        item['userUrl'] = user_data['user_url']

        yield item
