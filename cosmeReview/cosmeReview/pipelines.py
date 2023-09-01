import csv
from .items import reviewItem
from datetime import date


class CosmeReviewPipeline:
    def __init__(self):
        pass

    def open_spider(self, spider):
        filedate = date.today().strftime("%Y%m%d")
        filename = filedate + '_review.csv'
        self.filename = open(filename, mode='w', encoding='utf_8_sig', newline='')
        self.csv_analysis = csv.writer(self.filename, quoting=csv.QUOTE_ALL)
        self.csv_analysis.writerow(["Product ID", "Product Name", "Product URL", "Product Rating", "Product Ranking", "Brand ID", "Brand Name", "Brand URL", "Review ID","Review URL", "Review Rating", "Review Text", "User ID", "User Name", "User Age", "User URL"])

    def close_spider(self, spider):
        self.filename.close()

    def process_item(self, item, spider):
        if isinstance(item, reviewItem):
            self.csv_analysis.writerow([item['productId'], item['productName'], item['productUrl'], item['productRating'], item['productRanking'], item['brandId'], item['brandName'], item['brandUrl'], item['reviewId'], item['reviewUrl'], item['reviewRating'], item['reviewText'], item['userId'], item['userName'], item['userAge'], item['userUrl']])




