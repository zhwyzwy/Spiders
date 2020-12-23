import random
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from collections import namedtuple
ua = UserAgent()


class WechatSpider:
    """
    selenium  爬取搜狗微信平台
    """
    def __init__(self):
        self.url = 'https://weixin.sogou.com/weixin?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_='

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
        
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
        })
        return self.go_url(browser, keyword)

    def go_url(self, browser, keyword):

        browser.get(self.url.format(keyword))
        weixin_data = []
        elments = browser.find_elements_by_xpath("//ul[@class='news-list']/li")
        for elment in elments:
            elment.find_element_by_tag_name('h3 > a').click()
            time.sleep(2)
            
            new_window = browser.window_handles[-1] 
        
            browser.switch_to_window(new_window)    
            article = ''
            for i in browser.find_elements_by_xpath("//div[@id='js_content']/*"):
                article += i.text
            browser.close()
            new_window = browser.window_handles[0]
            browser.switch_to_window(new_window)

            data = namedtuple('weixin_art', ['keyword', 'title', 'article', 'plat', 'time'])
            data = data(keyword, elment.find_element_by_tag_name('h3 > a').text, article, elment.find_element_by_css_selector('.s-p > a').text,elment.find_element_by_css_selector('.s-p > span.s2').text)
            
            weixin_data.append(data)
        browser.quit()
        return weixin_data

    @staticmethod
    def main(keywords):
        resp_article = []
        for keyword in keywords:
            app = WechatSpider()
            req_article = app.browser_ini(keyword=keyword)
            resp_article = [{"keyword": article.keyword,
                             "title": article.title,
                             "content": article.article,
                             "type": '微信'} for article in req_article]
        return resp_article


if __name__ == '__main__':
    a = WechatSpider.main(['seo'])
    print(a)






