import scrapy, json
from w3lib.http import basic_auth_header
import logging
import time
import random
import xlrd
import pandas as pd
from hpd.items import HpdItem

class HPDSpider(scrapy.Spider):
    name = "hpd"
    count = 1
    start_urls = [
        'https://www1.nyc.gov/site/hpd/about/hpd-online.page'
    ]
    proxies = [
        'http://mehmet:shahrukh31@us-wa.proxymesh.com:31280',
        'http://mehmet:shahrukh31@fr.proxymesh.com:31280:31280',
        'http://mehmet:shahrukh31@jp.proxymesh.com:31280',
        'http://mehmet:shahrukh31@au.proxymesh.com:31280',
        'http://mehmet:shahrukh31@de.proxymesh.com:31280',
    ]

    def start_requests(self):
        self.logger.info(">> Going to start search page <<")
        return [scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            meta={
                # 'proxy': random.choice(self.proxies)
            })]
    
    def parse(self, response):
        item = HpdItem()
        borough = ['', 'Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten island']
        self.logger.info("Going to read file -->> {}".format(self.file_link))
        rows = pd.read_csv('{}'.format(self.file_link))
        df = pd.DataFrame(rows, columns = ['StreetName', 'Borough', 'HouseNumber'])
        self.logger.info("We will search for {} rows".format(self.lines))
        for index, row in df.iterrows():
            if index > int(self.lines):
                break

            url = 'https://hpdonline.hpdnyc.org/HPDonline/provide_address.aspx?subject=&env_report=REMOTE_HOST%2CHTTP_ADDR%2CHTTP_USER_AGENT&bgcolor=%23FFFFFF&required=p2&p1={}&p2={}&p3={}'
            item['borough'] = row['Borough'].capitalize()
            item['house_number'] = row['HouseNumber']
            item['street_name'] = row['StreetName']
            url = url.format(borough.index(row['Borough'].capitalize()), row['HouseNumber'], row['StreetName'].replace(' ', '+'))
            item['source_url'] = url
            yield scrapy.Request(
                url=url,
                method="GET",
                callback=self.parse_data,
                dont_filter=True,
                meta={'item': item,
                'proxy': random.choice(self.proxies)}
            )

    def parse_data(self, response):
        item = response.meta['item']
        for i in range(1, 13):
            heading = response.xpath("//table[@id='mymaintable_BldgInfo']//tr[2]/td[{}]/text()".format(i)).getall()[0]
            value = response.xpath("//table[@id='mymaintable_BldgInfo']//tr[2]/td[{}]/span/text()".format(i)).getall()[0]
            
            if i==1:
                item['hpd_no'] = value
            elif i==2:
                item['range_'] = value  
            elif i==3:
                item['block'] = value  
            elif i==4:
                item['lot'] = value  
            elif i==5:
                item['cd'] = value  
            elif i==6:
                item['census_tract'] = value  
            elif i==7:
                item['stories'] = value  
            elif i==8:
                item['a_units'] = value  
            elif i==9:
                item['b_units'] = value  
            elif i==10:
                item['ownership'] = value  
            elif i==11:
                item['registration_no'] = value  
            elif i==12:
                item['class_'] = value

        yield item
