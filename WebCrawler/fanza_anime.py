import sys
sys.path.append('../')
import re
# from pyquery import PyQuery as pq#need install
from lxml import etree#need install
# from bs4 import BeautifulSoup#need install
import json
from urllib.parse import urlencode
from ADC_function import *
import difflib
from WebCrawler import amazon

def calSimi(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def getTitle(html):
    result = html.xpath("//*[@class='item fn']/text()")[0]

    return result

def getStudio(html):
    result = html.xpath("//td[contains(text(), 'メーカー')]/..//a/text()")[0]

    return result

def getSeries(html):
    result = html.xpath("//td[contains(text(), 'シリーズ')]/..//a/text()")
    if (len(result) > 0):
        result = html.xpath("//td[contains(text(), 'シリーズ')]/..//a/text()")[0]
    else:
        result = ""
    return result

def getRelease(html):
    result = html.xpath("//td[contains(text(), '発売日')]/..//*[@width='100%']/text()")[0]

    return result

def getYear(html):
    release = getRelease(html)
    try:
        result = str(re.search(r"\d{4}", release).group())
        return result
    except:
        return release

def getRuntime(html):
    result = html.xpath("//td[contains(text(), '収録時間')]/..//*[@width='100%']/text()")[0]

    return result

def getTag(html):
    result = html.xpath("//td[contains(text(), 'ジャンル')]/..//a/text()")

    return result

def getLabel(html):
    result = html.xpath("//td[contains(text(), 'レーベル')]/..//a/text()")[0]

    return result


def getCid(html):
    result = html.xpath("//td[contains(text(), '品番')]/..//*[@width='100%']/text()")[0]
    
    return result

def getCover(html):
    cid = getCid(html)
    result = f"https://pics.dmm.co.jp/mono/movie/adult/{cid}/{cid}pl.jpg"

    return result

def getCover_by_title(title):
    return amazon.getCover_small_by_title(title)

def getOutline(html):
    result = " ".join(html.xpath("//*[@class='mg-b20 lh4']/p/text()"))

    print(result)
    return result




def main(title):
    series = title.split(' ')[0].split('~')[0]
    html = "https://www.dmm.co.jp/mono/-/search/=/searchstr=" + series + "/"

    html = get_html(
        "https://www.dmm.co.jp/age_check/=/declared=yes/?{}".format(
            urlencode({"rurl": html})
        )
    )

    # html = get_html("https://www.dmm.co.jp/mono/-/search/=/searchstr=" + series + "/")
    # html = get_html("https://animehonpo.com/products/list?category_id=&tag_id=&name="+title)
    html = etree.fromstring(html, etree.HTMLParser())

    url_list = html.xpath("//*[@class='img']/../@href")
    item_list = html.xpath("//*[@class='img']/img/@alt")

    selection = 0
    simi = 0
    for i in range(len(item_list)):
        result = calSimi(item_list[i], title)
        if (result > simi):
            simi = result
            selection = i

    print(f"Selected {item_list[selection]}: {url_list[selection]}")

    html = get_html(
        "https://www.dmm.co.jp/age_check/=/declared=yes/?{}".format(
            urlencode({"rurl": url_list[selection]})
        )
    )
    html = etree.fromstring(html, etree.HTMLParser())

    cover = getCover_by_title(getTitle(html))

    dic = {
        'actor': [],
        "actor_photo": "",
        'title': getTitle(html),
        'studio': getStudio(html),
        'outline': getOutline(html),
        'runtime': getRuntime(html),
        'release': getRelease(html),
        'number': getTitle(html),
        'cover': cover,
        # 'thumb': cover,
        'imagecut': 0,
        'director': '',
        'tag': getTag(html),
        "label": getLabel(html),
        'year': getYear(html),
        'website': url_list[selection],
        'source': 'fanza_anime.py',
        'series': getSeries(html),
    }

    if dic["series"] == "":
        dic["series"] = series

    js = json.dumps(
        dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(",", ":")
    )
    return js




if __name__ == "__main__":
    # title = "姫様LOVEライフ！ 生真面目ブルマ姫・ルリア～ワイセツおねだり王女♥～"
    title = "ボクと彼女（ナース）の研修日誌 THE ANIMATION"
    print(main(title))
    # html = get_html("https://animehonpo.com/products/list?category_id=&tag_id=&name="+title)


    # series = title.split(' ')[0].split('~')[0]
    # html = "https://www.dmm.co.jp/mono/-/search/=/searchstr=" + series + "/"

    # html = get_html(
    #     "https://www.dmm.co.jp/age_check/=/declared=yes/?{}".format(
    #         urlencode({"rurl": html})
    #     )
    # )

