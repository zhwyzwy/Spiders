# coding:utf-8
import re
import requests
import hashlib
import json
import execjs
import time
import urllib
import spider_config


class ZhiHuSpider(object):

    @staticmethod
    def sendRequest(keyword):
        keyword = urllib.parse.quote(keyword)
        url = "/api/v4/search_v3?t=general&q={keyword}&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0".format(keyword=keyword)
        referer = "https://www.zhihu.com/search?type=content&q={keyword}".format(keyword=keyword)
        salt = "+".join(['3_2.0', url, referer, spider_config.ZHIHU_COOKIE])
        genemd5 = hashlib.new('md5', salt.encode()).hexdigest()
        with open('g_encrypt.js', 'r') as f:
            ctx1 = execjs.compile(f.read(), cwd=r'/usr/local/lib/node/lib/node_modules')

        encrypt_str = ctx1.call("b", genemd5)

        headers = {
            'referer': referer,
            'user-agent': spider_config.UserAgent().random,
            'cookie': 'd_c0="ACBaJW67SBKPTi2AhkI6gtBmYuAgbBm-Kzk=|1606898617";',
            'x-api-version': '3.0.91',
            'x-zse-83': '3_2.0',
            'x-zse-86': '1.0_%s' % encrypt_str
        }
        req = requests.get("https://www.zhihu.com" + url, headers=headers)
        time.sleep(3)
        try:
            contents = json.loads(req.content.decode())
            return contents
        except json.decoder.JSONDecodeError as e:
            return None

    @staticmethod
    def parseData(contents, keyword):
        if contents is None:
            return None
        parse_con = [content['object'] for content in contents['data']
                     if content.get('object', None) is not None
                     and content['object'].get('type', None) == 'article'
                     ]

        res_list = [{'keyword': keyword,
                     'title': re.sub('<[^>]+>', '', content['title']),
                     'content': re.sub('<[^>]+>', '', content['content']),
                     'type': '知乎'
                     }
                    for content in parse_con
                    ]

        return res_list

    @staticmethod
    def main(keywords):
        res_list = []
        for keyword in keywords:
            req_list = ZhiHuSpider.parseData(ZhiHuSpider.sendRequest(keyword), keyword)
            if req_list is None:
                continue
            res_list += req_list
        return res_list


if __name__ == '__main__':
    res_list = ZhiHuSpider.main(['seo', "oa"])
    print(res_list)



