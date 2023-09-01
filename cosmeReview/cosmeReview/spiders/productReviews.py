import scrapy
from ..utils import LinkDetails, textHandler
from ..items import reviewItem

class cosmeSpider(scrapy.Spider):

    name = 'review'
    allowed_domains = ['www.cosme.net']
    

    def start_requests(self):

        yield scrapy.Request(
            url='https://www.cosme.net/categories/item/802/ranking/',
            callback=self.parse_product
        )


    def parse_product(self, response):
        product_divs = response.css("div.keyword-ranking-item dl.clearfix")
  
        for product_div in product_divs:

            product_name = product_div.css("dd.summary h4.item a::text").get()
            product_name = textHandler()._filter_text(product_name)

            product_url = product_div.css("dd.summary h4.item a::attr(href)").get()
            if product_url:
                product_id = LinkDetails(product_url).get_product_id()

            product_rating = product_div.css("dd.summary div.rating-point p.rating span::text").get()
            product_rating = textHandler()._filter_text(product_rating)

            brand_name = product_div.css("dd.summary div.clearfix span.brand a::text").get()
            brand_name = textHandler()._filter_text(brand_name)

            brand_url = product_div.css("dd.summary div.clearfix span.brand a::attr(href)").get()
            if brand_url:
                brand_id = LinkDetails(brand_url).get_brand_id()

            if product_id:
                review_page_url = f"https://www.cosme.net/products/{product_id}/review/"

            product_ranking = product_div.css("dt span.rank-num span.num::text").get()
            product_ranking = textHandler()._filter_text(product_ranking)
            if not product_ranking:
                product_ranking = product_div.css("dt span.rank-num img::attr(alt)").get()


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
            break
            

    def parse_reviews(self, response):
        review_links = response.css("div.review-sec p.read span a::attr(href)").getall()

        for review_link in review_links:
            review_id = LinkDetails(review_link).get_review_id()

            if review_id:
                review_url = f"https://www.cosme.net/reviews/{review_id}/"


            yield scrapy.Request(
                url=review_url,
                callback=self.parse_review,
                meta={
                    "product_data" : response.request.meta["product_data"],
                    "review_url" : review_url,
                    "review_id" : review_id
                }
            )

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


        user_url = response.css("div.review-sec div.head div.reviewer-info a::attr(href)").get()
        user_id = None
        if user_url:
            user_id = LinkDetails(user_url).get_user_id()

        user_name = response.css("div.review-sec div.head div.reviewer-info span.reviewer-name::text").get()
        user_name = textHandler()._filter_text(user_name)

        user_age = response.css("div.review-sec div.head div.reviewer-info ul")
        if user_age:
            user_age = user_age[0].css("li::text")
            if user_age:
                user_age = user_age[0].get()
                user_age = textHandler()._filter_text(user_age)


        review_rating = response.css("div.review-sec div.body div.rating p.reviewer-rating::text").get()
        review_rating = textHandler()._filter_text(review_rating)


        review_text = response.css("div.review-sec div.body p.read::text").getall()
        review_text = textHandler()._filter_text(review_text)

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

        item['reviewId'] = response.request.meta['review_id']
        item['reviewUrl'] = response.request.meta['review_url']
        item['reviewRating'] = review_rating
        item['reviewText'] = review_text

        item['userId'] = user_id
        item['userName'] = user_name
        item['userAge'] = user_age
        item['userUrl'] = user_url

        yield item
