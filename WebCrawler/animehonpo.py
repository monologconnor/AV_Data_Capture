import sys
sys.path.append('../')
import re
# from pyquery import PyQuery as pq#need install
from lxml import etree#need install
# from bs4 import BeautifulSoup#need install
import json
from ADC_function import *
import difflib
# from WebCrawler import fanza

def calSimi(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def getTitle(html):
    result = html.xpath("//*[@id='item_detail']//*[@class='item_name']/text()")

    return result

def getStudio(html):
    result = html.xpath("//*[@class='product_tag_list']/text()")[-1]

    return result







def main(title):
    html = get_html("https://animehonpo.com/products/list?category_id=&tag_id=&name="+title)
    html = etree.fromstring(html, etree.HTMLParser())

    url_list = html.xpath("//*[@class='product_item']/a/@href")
    item_list = html.xpath("//*[@class='product_item']//*[@class='item_name']/text()")

    selection = 0
    simi = 0
    for i in range(len(item_list)):
        result = calSimi(item_list[i], title)
        if (result > simi):
            simi = result
            selection = i

    print(f"Selected {item_list[selection]}: {url_list[selection]}")

    html = get_html(url_list[selection])
    html = etree.fromstring(html, etree.HTMLParser())

    # dic = {
    #     'title': 
    # }





if __name__ == "__main__":
    title = "OVAちーちゃん開発日記 ＃1"
    # main(title)
    html = get_html("https://animehonpo.com/products/list?category_id=&tag_id=&name="+title)