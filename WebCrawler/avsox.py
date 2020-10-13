import sys
sys.path.append('..')
import re
from lxml import etree
import json
from bs4 import BeautifulSoup
from ADC_function import *
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, errors = 'replace', line_buffering = True)

def getActorPhoto(htmlcode): #//*[@id="star_qdt"]/li/a/img
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'avatar-box'})
    d = {}
    for i in a:
        l = i.img['src']
        t = i.span.get_text()
        p2 = {t: l}
        d.update(p2)
    return d
def getTitle(a):
    try:
        html = etree.fromstring(a, etree.HTMLParser())
        result = str(html.xpath('/html/body/div[2]/h3/text()')).strip(" ['']") #[0]
        return result.replace('/', '')
    except:
        return ''
def getActor(a): #//*[@id="center_column"]/div[2]/div[1]/div/table/tbody/tr[1]/td/text()
    soup = BeautifulSoup(a, 'lxml')
    a = soup.find_all(attrs={'class': 'avatar-box'})
    d = []
    for i in a:
        d.append(i.span.get_text())
    return d
def getStudio(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//p[contains(text(),"制作商: ")]/following-sibling::p[1]/a/text()')).strip(" ['']").replace("', '",' ')
    return result1
def getRuntime(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//span[contains(text(),"长度:")]/../text()')).strip(" ['分钟']")
    return result1
def getLabel(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//p[contains(text(),"系列:")]/following-sibling::p[1]/a/text()')).strip(" ['']")
    return result1
def getNum(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//span[contains(text(),"识别码:")]/../span[2]/text()')).strip(" ['']")
    return result1
def getYear(release):
    try:
        result = str(re.search('\d{4}',release).group())
        return result
    except:
        return release
def getRelease(a):
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//span[contains(text(),"发行时间:")]/../text()')).strip(" ['']")
    return result1
def getCover(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[2]/div[1]/div[1]/a/img/@src')).strip(" ['']")
    return result
def getCover_small(htmlcode, number):
    javbus = get_html(f"https://www.javbus.com/{number}")
    javbus = etree.fromstring(javbus, etree.HTMLParser())
    result = javbus.xpath("//*[@class='sample-box']/@href")
    if len(result) != 0:
        result = result[0]
    else:
        html = etree.fromstring(htmlcode, etree.HTMLParser())
        result = str(html.xpath('//*[@id="waterfall"]/div/a/div[1]/img/@src')).strip(" ['']")
    return result
def getTag(a):  # 获取演员
    soup = BeautifulSoup(a, 'lxml')
    a = soup.find_all(attrs={'class': 'genre'})
    d = []
    for i in a:
        d.append(i.get_text())
    return d

def getSeries(htmlcode):
    try:
        html = etree.fromstring(htmlcode, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        result1 = str(html.xpath('//span[contains(text(),"系列:")]/../span[2]/text()')).strip(" ['']")
        return result1
    except:
        return ''

def getOutline(html):
    result = html.xpath('//*[@class="product-description mt-20"]/p/text()')[0]

    return result      

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



def main(number):
    html = get_html('https://tellme.pw/avsox')
    site = etree.HTML(html).xpath('//div[@class="container"]/div/a/@href')[0]
    a = get_html(site + '/cn/search/' + number)
    html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    result1 = str(html.xpath('//*[@id="waterfall"]/div/a/@href')).strip(" ['']")
    if result1 == '' or result1 == 'null' or result1 == 'None':
        a = get_html(site + '/cn/search/' + number.replace('-', '_'))
        html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        result1 = str(html.xpath('//*[@id="waterfall"]/div/a/@href')).strip(" ['']")
        if result1 == '' or result1 == 'null' or result1 == 'None':
            a = get_html(site + '/cn/search/' + number.replace('_', ''))
            html = etree.fromstring(a, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
            result1 = str(html.xpath('//*[@id="waterfall"]/div/a/@href')).strip(" ['']")
    web = get_html(result1)
    soup = BeautifulSoup(web, 'lxml')
    info = str(soup.find(attrs={'class': 'row movie'}))

    hcode_search = get_html('https://www.aventertainments.com/ppv/ppv_searchproducts.aspx?languageID=2&vodtypeid=1&keyword=' + number)
    html_search = etree.fromstring(hcode_search, etree.HTMLParser())
    search_result = getProduct(html_search, number)
    search_result = get_html(search_result)
    search_result = etree.fromstring(search_result, etree.HTMLParser())


    dic = {
        'actor': getActor(web),
        'title': getTitle(web).strip(getNum(web)),
        'studio': getStudio(info),
        'outline': getOutline(search_result),#
        'runtime': getRuntime(info),
        'director': '', #
        'release': getRelease(info),
        'number': getNum(info),
        'cover': getCover(web),
        'cover_small': getCover_small(a, number),
        'thumb': getCover(web),
        'imagecut': 3,
        'tag': getTag(web),
        'label': getLabel(info),
        'year': getYear(getRelease(info)),  # str(re.search('\d{4}',getRelease(a)).group()),
        'actor_photo': getActorPhoto(web),
        'website': result1,
        'source': 'avsox.py',
        'series': getSeries(info),
    }
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js

if __name__ == "__main__":
    print(main('043020_001'))
