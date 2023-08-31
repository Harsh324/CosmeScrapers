# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import date
import csv

class CosmereviewPipeline:
    def __init__(self):
        pass

    def open_spider(self, spider):
        filedate = date.today().strftime("%Y%m%d")
        filename = filedate + '_product_reviews.csv'
        self.filename = open(filename, mode='w', encoding='utf_8_sig')
        self.csv_analysis = csv.writer(self.filename, quoting=csv.QUOTE_ALL)
        self.csv_analysis.writerow(['サイトID', 'プランID', 'url', '収集日', '検索日', 'TOP画像URL', '会員価格', '通常価格', '残り部屋数', 'プラン名', 'プラン基本情報', 'プラン詳細情報', '客室名', '客室タグ', '客室基本情報', '人数', 'ポイント'])

    def close_spider(self, spider):
        self.filename.close()

    def process_item(self, item, spider):
    
        product_data = item['product_data']
        review_data = item['review_data']
        user_data = item['user_data']
        
        self.csv_analysis.writerow([
            product_data.get("product_name", ""),
            product_data.get("product_url", ""),
            product_data.get("product_id", ""),
            product_data.get("product_rating", ""),
            product_data.get("brand_name", ""),
            product_data.get("brand_url", ""),
            product_data.get("brand_id", ""),
            product_data.get("review_page_url", ""),
            review_data.get("review_id", ""),
            review_data.get("review_url", ""),
            review_data.get("review_rating", ""),
            review_data.get("review_text", ""),
            user_data.get("user_id", ""),
            user_data.get("user_name", ""),
            user_data.get("user_age", ""),
            user_data.get("user_url", "")
        ])

        return item


