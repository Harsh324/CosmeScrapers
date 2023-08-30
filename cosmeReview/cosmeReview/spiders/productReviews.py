import scrapy
from ..utils import LinkDetails

class cosmeSpider(scrapy.Spider):

    name = 'review'
    allowed_domains = ['www.cosme.net']
    

    def start_requests(self):

        yield scrapy.Request(
            url='https://www.cosme.net/categories/item/802/ranking/',
            callback=self.parse_product
        )


    def parse_product(self, response):
        product_divs = response.css("div.keyword-ranking-item dl.clearfix dd.summary")
  
        for product_div in product_divs:

            product_name = product_div.css("h4.item a::text").get()
            product_url = product_div.css("h4.item a::attr(href)").get()
            product_id = LinkDetails(product_url).get_product_id()
            product_rating = product_div.css("div.rating-point p.rating span::text").get()
            brand_name = product_div.css("div.clearfix span.brand a::text").get()
            brand_url = product_div.css("div.clearfix span.brand a::attr(href)").get()
            brand_id = LinkDetails(brand_url).get_brand_id()
            
            review_page_url = f"https://www.cosme.net/products/{product_id}/review/"


            yield scrapy.Request(
                url=review_page_url, 
                callback=self.parse_reviews, 
                meta={
                    "product_data" : {
                        "product_name": product_name,
                        "product_url": product_url,
                        "product_id": product_id,
                        "product_rating": product_rating,
                        "brand_name": brand_name,
                        "brand_url": brand_url,
                        "brand_id": brand_id,
                        "review_page_url" : review_page_url
                    }
                }
            )
            

    def parse_reviews(self, response):
        review_links = response.css("div.review-sec p.read span a::attr(href)").getall()

        for review_link in review_links:
            review_id = LinkDetails(review_link).get_review_id()

            review_url = f"https://www.cosme.net/reviews/{review_id}/"



            yield scrapy.Request(
                url=review_url,
                callback=self.parse_review,
                meta={
                    "product_data" : response.request.meta['product_data'],
                    "review_url" : review_url,
                    "review_id" : review_id
                }
            )



    def parse_review(self, response):

        product_ranking = response.css("div.info div.info-desc span.info-ranking span::text").get() # returns the ranking of the product

        user_url = response.css("div.review-sec div.head div.reviewer-info a::attr(href)").get() # returns the link of the user_details page of the reviewer
        user_id = LinkDetails(user_url).get_user_id()
        user_name = response.css("div.review-sec div.head div.reviewer-info span.reviewer-name::text").get()
        user_age = response.css("div.review-sec div.head div.reviewer-info ul")[0].css("li::text")[0].get()


        review_rating = response.css("div.review-sec div.body div.rating p.reviewer-rating::text").get() # returns rating of the product given by the reviewer
        review_texts = response.css("div.review-sec div.body p.read::text").getall() # returns list of texts
        
        review_text = ""
        for text in review_texts:
            review_text += text

        product_data = response.request.meta['product_data']
        product_data["product_ranking"] = product_ranking

        yield {
            "product_data" : product_data,

            "review_data" : {
                "review_id" : response.request.meta['review_id'],
                "review_url" : response.request.meta['review_url'],
                "review_rating" : review_rating,
                "review_text" : review_text
            },

            "user_data" : {
                "user_id" : user_id,
                "user_name" : user_name,
                "user_age" : user_age,
                "user_url" : user_url
            }
        }
