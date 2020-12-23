# coding:utf-8
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from collections import namedtuple
ua = UserAgent()


class SouHuSpider(object):
    """
    selenium  爬取搜狗微信平台
    """
    def __init__(self):
        self.url = 'https://search.sohu.com/?queryType=outside&keyword=seo&spm=smpc.home.0.0.1608635708355ueVtcja'

    def browser_ini(self, keyword):
        chrome_opt = Options()
        chrome_opt.add_argument("headless")
        chrome_opt.add_argument('--no-sandbox')
        chrome_opt.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_opt.add_experimental_option('useAutomationExtension', False)

        chrome_opt.add_argument('--disable-gpu')
        chrome_opt.add_argument('--disable-dev-shm-usage')
        chrome_opt.add_argument('--user-agent={}'.format(ua.random))
        browser = webdriver.Chrome(options=chrome_opt, executable_path='{}/chromedriver'.format(os.path.abspath(os.path.dirname(__file__))))
    
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source":
                                                                              """
                                                                              Object.defineProperty(navigator, 'webdriver', {get: () => undefined})
                                                                              """
                                                                          }
                                )
        return self.go_url(browser, keyword)

    def go_url(self, browser, keyword):
        browser.get(self.url.format(keyword=keyword))
        time.sleep(3)
        weixin_data = []
        elments = browser.find_elements_by_xpath('//div[@id="news-list"]/div')[:-1]
        for elment in elments:
            elment.find_element_by_tag_name('div.cards-content-title > a').click()
            title = elment.find_element_by_tag_name('div.cards-content-title').text
            time.sleep(2)
            new_window = browser.window_handles[-1]
            browser.switch_to_window(new_window)
            article = ''
            for i in browser.find_elements_by_xpath("//*[@id='mp-editor']/*"):
                article += i.text
            times = browser.find_element_by_xpath('//*[@id="news-time"]').text
            browser.close()
            new_window = browser.window_handles[0]
            browser.switch_to_window(new_window)
            data = namedtuple('weixin_art', ['keyword', 'title', 'article', 'time'])
            data = data(keyword, title, article, times)
            weixin_data.append(data)
        browser.quit()
        return weixin_data

    @staticmethod
    def main(keywords):
        resp_article = []
        for keyword in keywords:
            app = SouHuSpider()
            req_article = app.browser_ini(keyword=keyword)
            resp_article = [{"keyword": article.keyword,
                             "title": article.title,
                             "content": article.article,
                             "type": '搜狐'} for article in req_article]
        return resp_article


if __name__ == '__main__':
    a = SouHuSpider.main(['seo', 'oa'])
    print(a)


