import sys
sys.path.append('../')
import re
from pyquery import PyQuery as pq#need install
from lxml import etree#need install
from bs4 import BeautifulSoup#need install
import json
from ADC_function import *
from WebCrawler import fanza
from WebCrawler import javdb
from WebCrawler import amazon
from WebCrawler import airav

def getActorPhoto(htmlcode): #//*[@id="star_qdt"]/li/a/img
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'star-name'})
    d={}
    for i in a:
        l=i.a['href']
        t=i.get_text()
        html = etree.fromstring(get_html(l), etree.HTMLParser())
        p=str(html.xpath('//*[@id="waterfall"]/div[1]/div/div[1]/img/@src')).strip(" ['']")
        p2={t:p}
        d.update(p2)
    return d
def getTitle(htmlcode):  #获取标题
    # doc = pq(htmlcode)
    # title=str(doc('div.container h3').text()).replace(' ','-')
    # try:
    #     title2 = re.sub('n\d+-','',title)
    #     return title2
    # except:
    #     return title

    html = etree.fromstring(htmlcode, etree.HTMLParser())
    title = html.xpath("//*[@id='title']/text()")

    return title

def getStudio(htmlcode): #获取厂商 已修改
    html = etree.fromstring(htmlcode,etree.HTMLParser())
    # 如果记录中冇导演，厂商排在第4位
    if '製作商:' == str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[4]/span/text()')).strip(" ['']"):
        result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[4]/a/text()')).strip(" ['']")
    # 如果记录中有导演，厂商排在第5位
    elif '製作商:' == str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[5]/span/text()')).strip(" ['']"):
        result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[5]/a/text()')).strip(" ['']")
    else:
        result = ''
    return result
def getYear(htmlcode):   #获取年份
    html = etree.fromstring(htmlcode,etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')).strip(" ['']")
    return result
def getCover(htmlcode):  #获取封面链接
    doc = pq(htmlcode)
    image = doc('a.bigImage')
    return image.attr('href')
# def getCover_small(htmlcode):
#     html = etree.fromstring(htmlcode, etree.HTMLParser())
#     result =html.xpath("//*[@class='photo-frame']/img/@src")[0]
#     return result
def getCover_small(cid):
    result = f"https://pics.dmm.co.jp/digital/video/{cid}/{cid}ps.jpg"
    return result

def getCover_small_by_title(title):
    return amazon.getCover_small_by_title(title)

def getTrailer(number):
    return javdb.getTrailer_by_number(number)



def getRelease(htmlcode): #获取出版日期
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[2]/text()')).strip(" ['']")
    return result
def getRuntime(htmlcode): #获取分钟 已修改
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[3]/text()')).strip(" ['']分鐘")
    return result
def getActor(htmlcode):   #获取女优
    # b=[]
    # soup=BeautifulSoup(htmlcode,'lxml')
    # a=soup.find_all(attrs={'class':'star-name'})
    # for i in a:
    #     b.append(i.get_text())
    # return b
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    
    result = html.xpath('//*[@class="star-name"]/a/text()')

    return result

def getNum(htmlcode):     #获取番号
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[1]/span[2]/text()')).strip(" ['']")
    return result
def getDirector(htmlcode): #获取导演 已修改
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    if '導演:' == str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[4]/span/text()')).strip(" ['']"):
        result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[4]/a/text()')).strip(" ['']")
    else:
        result = ''         # 记录中有可能没有导演数据
    return result
def getCID(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    #print(htmlcode)
    string = html.xpath("//a[contains(@class,'sample-box')][1]/@href")[0].replace('https://pics.dmm.co.jp/digital/video/','')
    result = re.sub('/.*?.jpg','',string)
    return result
def getOutline(htmlcode):  #获取演员
    try:
        # response = json.loads(airav.main(number))
        # result = response['outline']
        # return result
        html = etree.fromstring(htmlcode, etree.HTMLParser())
        result = html.xpath("string(//div[contains(@class,'mg-b20 lh4')])").replace('\n','')
    except:
        result = ''
        
    return result
def getSerise(htmlcode):   #获取系列 已修改
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    # 如果记录中冇导演，系列排在第6位
    if '系列:' == str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[6]/span/text()')).strip(" ['']"):
        result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[6]/a/text()')).strip(" ['']")
    # 如果记录中有导演，系列排在第7位
    elif '系列:' == str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[7]/span/text()')).strip(" ['']"):
        result = str(html.xpath('/html/body/div[5]/div[1]/div[2]/p[7]/a/text()')).strip(" ['']")
    else:
        result = ''
    return result
def getTag(htmlcode):  # 获取标签
    tag = []
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'genre'})
    for i in a:
        if 'onmouseout' in str(i) or '多選提交' in str(i):
            continue
        tag.append(translateTag_to_sc(i.get_text()))
    return tag

def getThumb(cid, htmlcode):
    modified = cid.replace("00", '', 1)
    result = []
    result.append(f"https://pics.dmm.co.jp/mono/movie/adult/{modified}/{modified}pl.jpg")
    result.append(f"https://pics.dmm.co.jp/mono/movie/adult/{modified}so/{modified}sopl.jpg")
    result.append(f"https://pics.dmm.co.jp/mono/movie/adult/{cid}/{cid}pl.jpg")

    for item in result:
        html = get_html(item, return_type="object")
        if "now_printing" not in html.url:
            return item


    return getCover(htmlcode)

def getProduct_uncen(html, number):
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

def getOutline_uncen(html):
    result = html.xpath('//*[@class="product-description mt-20"]/p/text()')[0]

    return result

def getCover_uncen_small(html, number):
    result = html.xpath("//*[@class='sample-box']/@href")
    if len(result) != 0:
        result = result[0]
    else:
        html = f"https://www.javbus.com/uncensored/search/{number}"
        html = etree.fromstring(html, etree.HTMLParser())
        result = html.xpath("//*[@class='photo-frame']/img/@src")[0]
    return result
def getExtrafanart(htmlcode):  # 获取剧照
    html_pather = re.compile(r'<div id=\"sample-waterfall\">[\s\S]*?</div></a>\s*?</div>')
    html = html_pather.search(htmlcode)
    if html:
        html = html.group()
        extrafanart_pather = re.compile(r'<a class=\"sample-box\" href=\"(.*?)\"')
        extrafanart_imgs = extrafanart_pather.findall(html)
        if extrafanart_imgs:
            return extrafanart_imgs
    return ''

def main_uncensored(number):
    htmlcode = get_html('https://www.javbus.com/ja/' + number)
    if getTitle(htmlcode) == '':
        htmlcode = get_html('https://www.javbus.com/ja/' + number.replace('-','_'))
    
    avent_html = get_html('https://www.aventertainments.com/ppv/ppv_searchproducts.aspx?languageID=2&vodtypeid=1&keyword=' + number)
    html_search = etree.fromstring(avent_html, etree.HTMLParser())
    search_result = getProduct_uncen(html_search, number)
    avent_html = get_html(search_result)
    avent_html = etree.fromstring(htmlcode, etree.HTMLParser())

    title = str(re.sub('\w+-\d+-','',getTitle(htmlcode))).replace(getNum(htmlcode)+'-','')

    dic = {
        'title': title,
        'studio': getStudio(htmlcode),
        'year': getYear(htmlcode),
        'outline': getOutline_uncen(avent_html),
        'runtime': getRuntime(htmlcode),
        'director': getDirector(htmlcode),
        'actor': getActor(htmlcode),
        'release': getRelease(htmlcode),
        'number': getNum(htmlcode),
        'cover': getCover(htmlcode),
        'cover_small': getCover_uncen_small(htmlcode, number),
        'tag': getTag(htmlcode),
        'extrafanart': getExtrafanart(htmlcode),
        'label': getSerise(htmlcode),
        'imagecut': 3,
        'actor_photo': '',
        'website': 'https://www.javbus.com/ja/' + number,
        'source': 'javbus.py',
        'series': getSerise(htmlcode),
    }
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js


def main(number):
    # number = "DV-1326_2011-11-11"
    try:
        # try:
        try:
            htmlcode = get_html('https://www.fanbus.us/' + number)
        except:
            htmlcode = get_html('https://www.javbus.com/' + number)
        cid = getCID(htmlcode)
        try:
            dww_htmlcode = fanza.main_htmlcode(getCID(htmlcode))
        except:
            dww_htmlcode = ''
        # title = str(re.sub('\w+-\d+-', '', getTitle(htmlcode)))
        dic = {
            'title': getTitle(dww_htmlcode),
            'studio': getStudio(htmlcode),
            'year': str(re.search('\d{4}', getYear(htmlcode)).group()),
            'outline': getOutline(dww_htmlcode),
            'runtime': getRuntime(htmlcode),
            'director': getDirector(htmlcode),
            'actor': getActor(htmlcode),
            'release': getRelease(htmlcode),
            'number': getNum(htmlcode),
            'cover': getCover(htmlcode),
            'cover_small': getCover_small_by_title(title),
            'thumb': getThumb(cid, htmlcode),
            'trailer': getTrailer(number),
            'imagecut': 3,
            'tag': getTag(htmlcode),
            'extrafanart': getExtrafanart(htmlcode),
            'label': getSerise(htmlcode),
            'actor_photo': getActorPhoto(htmlcode),
            'website': 'https://www.javbus.com/' + number,
            'source': 'javbus.py',
            'series': getSerise(htmlcode),
        }

        if dic['cover'] == dic['thumb']:
            dic['imagecut'] = 3
            dic['cover_small'] = getCover_small(cid)

        js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4,separators=(',', ':'), )  # .encode('UTF-8')
        return js
        # except:
        #     return main_uncensored(number)
    except Exception as e:
        print(e)
        data = {
            "title": "",
        }
        js = json.dumps(
            data, ensure_ascii=False, sort_keys=True, indent=4, separators=(",", ":")
        )
        return js

if __name__ == "__main__" :
    # print(main('IPX-292'))
    print(main('SSNI-830'))
