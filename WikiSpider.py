import scrapy
from scrapy.crawler import CrawlerProcess
import mysql.connector #version 8.0.25

mydb = mysql.connector.connect(host = 'localhost',
                               user = 'root',
                               password = 'SU9887@',
                               database = 'private_deal')
cur = mydb.cursor()
print(mydb.connection_id)

#create table.
wtbl = """CREATE TABLE IF NOT EXISTS SCRAP_WIKI(area_name varchar(70) not null,
          description MEDIUMTEXT not null)"""
cur = mydb.cursor()
cur.execute(wtbl)
mydb.commit()
print("table create successfully")

class WikiSpider(scrapy.Spider):
    name = 'WikiSpider'
    start_urls = ['https://en.wikipedia.org/wiki/Main_Page']


    def parse(self, response):
        cur = mydb.cursor()
        are=[]
        des=[]
        areas = response.css('div#mp-other-content a::text').getall()
        description = response.css('div#mp-other-content li::text').getall()
       
        data = "INSERT INTO SCRAP_WIKI(area_name, description) values (%s,%s)"
        for a in areas:
            are.append(a)
        for d in description:
            des.append(d)
        for i in range(0,6):
            result=(are[i],des[i])
            cur.execute(data,result)
            mydb.commit()
        print("data stored")

#Run Spider.
pro = CrawlerProcess()
pro.crawl(WikiSpider)
pro.start()
