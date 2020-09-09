import re
from lxml import etree
import json
from bs4 import BeautifulSoup
import sys
sys.path.append('../')
from ADC_function import *
# htmlcode = get_html('https://www.dlsite.com/pro/work/=/product_id/' + 'VJ013517' + '.html',
#                             cookies={'locale': 'zh-cn'})
# html = etree.fromstring(htmlcode, etree.HTMLParser())

def main(number):
    try:
        number = number.replace('-', '_')
        print(f"searching {number}")
        number = number.upper()
        hcode_search = get_html('https://www.aventertainments.com/ppv/ppv_searchproducts.aspx?languageID=2&vodtypeid=1&keyword=' + number)
        html_search = etree.fromstring(hcode_search, etree.HTMLParser())
        
        search_result = getProduct(html_search, number)

        htmlcode = get_html(search_result)
        html = etree.fromstring(htmlcode, etree.HTMLParser())
        # dic = {
        #     'actor': None,
        #     'title': getTitle(html),
        #     'studio': None,
        #     'outline': None,
        # }
        # return html
        dic = {
            'actor': getActor(html),
            'title': getTitle(html),
            'studio': getStudio(html),
            'outline': getOutline(html),
            'runtime': getRuntime(html),
            'director': getDirector(html),
            'release': getRelease(html),
            'number': number,
            'cover': getCover(html),
            'cover_small': getCover_small(html),
            'imagecut': 3,
            'tag': getTag(html),
            'label': getLabel(html),
            'year': getYear(getRelease(html)),  # str(re.search('\d{4}',getRelease(a)).group()),
            'actor_photo': '',
            'website': search_result,
            'source': 'aventertainment.py',
            'series': getSeries(html),
        }
        js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
    except:
        data = {
            'title': "",
        }
        js = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(",", ":"))
    
    return js


def getProduct(html, number):
    product_name = html.xpath('//*[@class="product-title"]/a/text()')
    result = html.xpath('//*[@class="product-title"]/a/@href')
    if len(product_name) > 1:
        print(f"Multiple results found for {number}, choose one from them with the number:")
        for i in range(len(product_name)):
            print(f"({i}) {product_name[i]}")

        index = int(input(">>"))
    else:
        index = 0
    result = result[index]

    return result

def getTitle(html):
    result = html.xpath('//*[@class="section-title"]/h3/text()')[0]
    result = result.replace('(FullHD)', '')

    return result.strip()

def getActor(html):
    try:
        result = html.xpath('//span[contains(text(), "主演女優")]/../*[@class="value"]/a/text()')
    except:
        result = ''

    return result

def getActorPhoto(actor):
    actor_list = actor.split(',')
    d = {}
    for item in actor_list:
        photo = {item: ''}
        d.update(photo)
    
    return d 

def getStudio(html):
    result = html.xpath('//span[contains(text(), "スタジオ")]/../*[@class="value"]/a/text()')[0]
    return result

def getRuntime(html):
    result = html.xpath('//span[contains(text(), "収録時間")]/../*[@class="value"]/text()')[0]
    return result

def getLabel(html):
    result = html.xpath('//span[contains(text(), "シリーズ")]/../*[@class="value"]/a/text()')[0]
    return result

def getRelease(html):
    result = html.xpath('//span[contains(text(), "発売日")]/../*[@class="value"]/text()')[0]
    result = result.strip()
    return result

def getYear(release):
    year = release.split('/')[-1]
    return year

def getTag(html):
    result = html.xpath('//span[contains(text(), "カテゴリ")]/../*[@class="value-category"]/a/text()')

    return result

def getCover_small(html, index=0):
    result = html.xpath('//*[@class="lightbox"]/@href')[0]

    return result

def getCover(html):
    result = html.xpath('//*[@id="PlayerCover"]/img/@src')[0]

    return result

def getDirector(html):
    return ''

def getOutline(html):
    result = html.xpath('//*[@class="product-description mt-20"]/p/text()')[0]

    return result

def getSeries(html):
    result = html.xpath('//span[contains(text(), "シリーズ")]/../*[@class="value"]/a/text()')[0]

    return result


if __name__ == "__main__":
    input_num = '043020_001'
    # print("")
    code = main(input_num)
    print(code)