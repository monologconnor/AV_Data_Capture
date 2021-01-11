import sys
sys.path.append('../')
import re
# from pyquery import PyQuery as pq#need install
from lxml import etree
# from bs4 import BeautifulSoup#need install
import json
from urllib.parse import urlencode
from ADC_function import *
import difflib


cookie = {
    "session-id": "356-8483597-6837505",
    "ubid-acbjp": "357-7833949-7568744",
    "lc-acbjp": "ja_JP",
    "i18n-prefs": "JPY",
    "x-acbjp": "osZdj4nQnYuhQlegHEz57Mj?7ss1?2caZ98mRxvvgNAwAOo49UiAPcLZYg4ZuLOg",
    "session-token": "zNaHVy4mZfXD/M+5XhHxKtDdqYkbpF0RAFd6OM+lTdu8ZR2lS3KftNM6TZySUNpw5cm70Wahpq3C8vZFp62lb7myEltToqzhKFuXm8pyixu58AXH8/oa6Ne6u8cjUNlq9kA/Nxu75bz1cJWJV17ytB7y03hyjoRn0h83/1EiYlUi0YHNbS7qU/Czs+am0E1sVaPCye5jzXoev0bYzodyHQ==",
    "session-id-time": "2082787201l",
    "csm-hit=tb":"4M8XK5K96BNJT3YDTA87+s-4M8XK5K96BNJT3YDTA87|1610215808070&t:1610215808070&adb:adblk_yes"
}

def calSimi(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def getCover_small(html):
    result =  html.xpath("//*[@id='imgTagWrapperId']/img/@data-old-hires")[0]
    return result

def getTitle(html):
    result = html.xpath("//*[@id='productTitle']/text()")[0].strip().replace(" [DVD]", "")
    return result

def getCover_small_by_title(title):
    cookie = {
        "session-id": "356-8483597-6837505",
        "ubid-acbjp": "357-7833949-7568744",
        "lc-acbjp": "ja_JP",
        "i18n-prefs": "JPY",
        "x-acbjp": "osZdj4nQnYuhQlegHEz57Mj?7ss1?2caZ98mRxvvgNAwAOo49UiAPcLZYg4ZuLOg",
        "session-token": "zNaHVy4mZfXD/M+5XhHxKtDdqYkbpF0RAFd6OM+lTdu8ZR2lS3KftNM6TZySUNpw5cm70Wahpq3C8vZFp62lb7myEltToqzhKFuXm8pyixu58AXH8/oa6Ne6u8cjUNlq9kA/Nxu75bz1cJWJV17ytB7y03hyjoRn0h83/1EiYlUi0YHNbS7qU/Czs+am0E1sVaPCye5jzXoev0bYzodyHQ==",
        "session-id-time": "2082787201l",
        "csm-hit=tb":"4M8XK5K96BNJT3YDTA87+s-4M8XK5K96BNJT3YDTA87|1610215808070&t:1610215808070&adb:adblk_yes"
    }

    htmlcode = get_html("https://www.amazon.co.jp/s?k=" + title, cookies=cookie)
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    url_list = html.xpath("//*[@class='a-size-base-plus a-color-base a-text-normal']/../@href")
    item_list = html.xpath("//*[@class='a-size-base-plus a-color-base a-text-normal']/text()")

    selection = 0
    simi = 0
    for i in range(len(item_list)):
        result = calSimi(item_list[i], title)
        if (result > simi):
            simi = result
            selection = i

    print(f"Selected {item_list[selection]}")
    
    htmlcode = get_html(f"https://www.amazon.co.jp/{url_list[selection]}")
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = html.xpath('//*[@class="alert"]/../div/a/@href')[0]
    htmlcode = get_html(result, cookies=cookie)

    html = etree.fromstring(htmlcode, etree.HTMLParser())

    return getCover_small(html)

def getOutline(html):
    result = '\n'.join(html.xpath("//*[@id='productDescription']/p/text()"))
    result = result.replace('<', '[').replace('>', ']')
    # result = result.replace('<STORY>', '[STORY]')
    return result


def getUrl_html(title):
    htmlcode = get_html("https://www.amazon.co.jp/s?k=" + title, cookies=cookie)
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    url_list = html.xpath("//*[@class='a-size-base-plus a-color-base a-text-normal']/../@href")
    item_list = html.xpath("//*[@class='a-size-base-plus a-color-base a-text-normal']/text()")

    selection = 0
    simi = 0
    for i in range(len(item_list)):
        result = calSimi(item_list[i], title)
        if (result > simi):
            simi = result
            selection = i

    print(f"Selected {item_list[selection]}: {url_list[selection]}")
    url = f"https://www.amazon.co.jp/{url_list[selection]}"
    return get_html(url, cookies=cookie)


def main(title):

    htmlcode = get_html("https://www.amazon.co.jp/s?k=" + title, cookies=cookie)
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    url_list = html.xpath("//*[@class='a-size-base-plus a-color-base a-text-normal']/../@href")
    item_list = html.xpath("//*[@class='a-size-base-plus a-color-base a-text-normal']/text()")

    selection = 0
    simi = 0
    for i in range(len(item_list)):
        result = calSimi(item_list[i], title)
        if (result > simi):
            simi = result
            selection = i

    print(f"Selected {item_list[selection]}: {url_list[selection]}")
    
    htmlcode = get_html(f"https://www.amazon.co.jp/{url_list[selection]}")
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = html.xpath('//*[@class="alert"]/../div/a/@href')[0]
    htmlcode = get_html(result, cookies=cookie)

    html = etree.fromstring(htmlcode, etree.HTMLParser())

    return htmlcode





# html.xpath('//*[@class="alert"]/../div/a/@href')[0]


    # pass

if __name__ == "__main__":
    # html = main("ボクと彼女（ナース）の研修日誌 THE ANIMATION")
    # html = main("アイベヤ THE ANIMATION")
    # html = main("SSNI-830 股下3センチ美脚タイトミニスカナースの誘惑 星宮一花")
    amazon_url = getUrl_html("股下3センチ美脚タイトミニスカナースの誘惑 星宮一花")
    pass