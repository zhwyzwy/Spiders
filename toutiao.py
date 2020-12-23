import requests
import re
import time
from urllib.parse import urlencode
from lxml import etree
from common.libs.spiders import spider_config


class TouTiaoSpider(object):
    def __init__(self, keyword):
        spider_config.TOUTIAO_PARAMS['keyword'] = keyword
        self.keyword = keyword
        self.toutiao_url = 'https://www.toutiao.com/api/search/content/?' + urlencode(spider_config.TOUTIAO_PARAMS)

    def toutiao_article_url(self):
        resp = requests.get(url=self.toutiao_url, headers=spider_config.HEADERS)
        if resp.status_code != 200:
            return None
        return resp.json()

    def toutiao_parse_url(self):

        resp_data = self.toutiao_article_url()
        if resp_data is None:
            return None

        for article_data in resp_data.get('data'):
            if all([article_data.get('article_url'), article_data.get('has_video')==False]):
                resp = requests.get(url=article_data['article_url'], headers=spider_config.HEADERS, cookies=spider_config.TOUTIAO_COOKIE)
                time.sleep(3)
                parser_html = etree.HTML(resp.text)
                # return parser_html
                yield parser_html
            else:
                # pass
                yield

    def toutiao_articles_content(self):
        parse_html = self.toutiao_parse_url()
        if parse_html is None:
            return None
        for parse in parse_html:
            if parse is None:
                continue
            try:
                title = parse.xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]/h1')[0].text
                bloger = parse.xpath('//*[@id="root"]/div/div[2]/div[1]/div[2]/article')

                info = bloger[0].xpath('string(.)')
                # return [self.keyword, title, info]
                yield [self.keyword, title, info]
            except Exception as e:
                pass

            try:
                title = parse.xpath('/html/body/div[2]/div[2]/h1')[0].text
                bloger = parse.xpath('/html/body/div[2]/div[3]/div[3]')
                info = bloger[0].xpath('string(.)')
                # return [self.keyword, title, info]
                yield [self.keyword, title, info]

            except Exception as e:
                pass

    @staticmethod
    def main(keywords):
        articles_list = []
        contents = []
        for keyword in keywords:
            toutiao = TouTiaoSpider(keyword)
            contents += list(toutiao.toutiao_articles_content())
        for content in contents:
            if content is None:
                continue
            articles_list.append({'keyword': content[0],
                             'title': re.sub(r'<[^>]+>', '', content[1]),
                             'content': re.sub(r'<[^>]+>', '', content[2]),
                             'type': '头条',
                             })
        return articles_list


if __name__ == '__main__':
    articles = TouTiaoSpider.main(['rpa', "钓鱼"])
    print(articles)








