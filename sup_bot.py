__author__ = 'maxim'

import requests
from bs4 import BeautifulSoup
import webbrowser
import timing

#TODO: move to interface

BASE = 'http://www.supremenewyork.com/'
SHOP_DIR = "shop/"
CART_DIR = "cart/"
ALL_DIR = "all/"

'''
DEPARTMENT = "t-shirts"
ITEM = "Kiss Tee"
COLOR = "Lime"
ITEM_SIZE = 'Medium'
ORDER_MAIL = 'test@example.com'
FIRST_NAME = 'test'
LAST_NAME = 'test'
COMPANY_NAME = 'test'
ADDRESS_1 = 'test 123'
ADDRESS_2 = ''
CITY_NANE = 'Agoura'
ZIP = '91376'
COUNTRY = 'United States'
PROVINCE = 'California'
PHONE = '32532456'
CART_LINK = 'http://shop.kithnyc.com/cart'
CREDIT_CARD_NUM = '4272123345674941'
CREDIT_CARD_FIRST_NAME = 'test'
CREDIT_CARD_LAST_NAME = 'test'
CREDIT_CARD_MONTH = '1'
CREDIT_CARD_YEAR = '2015'
CREDIT_CARD_CVV2 = '243'
'''
class SupBot:

    from datetime import datetime, time
    from time import sleep


    def wait_start(self, runTime):
        startTime = time(*(map(int, runTime.split(':'))))
        while startTime > datetime.today().time(): # you can add here any additional variable to break loop if necessary
            sleep(1)# you can change 1 sec interval to any other
        return

    def _get_item_page(self, item_page_html):
        parsed_page = BeautifulSoup(item_page_html)
        div = parsed_page.body.find('div', id="wrap")
        div = div.find('div', id='container')
        for item in div.findAll('article'):
            if item.div.h1.a.find(text=ITEM) and item.div.p.a.find(text=COLOR):
                return item.div.a['href']
        return None

    def _get_item_id(self, item_page_html):
        parsed_page = BeautifulSoup(item_page_html)
        div = parsed_page.body.find('div', id="wrap")
        div = div.find('div', id='container')
        div = div.find('div', id='details')
        style_id = div.div.form.find('input', id='style')['value']
        fieldset = div.div.form.find('fieldset', class_=None)
        link = div.div.form['action']
        select = fieldset.find('select')
        size_elem = select.find('option', text=ITEM_SIZE)

        return {'style':style_id,'size':size_elem['value'], 'link':link}

    def checkout(self, item_name):

        http_proxy  = "http://46.101.72.191:8118"


        proxyDict = {
                      "http"  : http_proxy
                    }

        from selenium import webdriver
        from selenium.webdriver.support.ui import Select
        driver = webdriver.Firefox()
        driver.get("https://www.supremenewyork.com")



        #self.wait_start('15:40:20')

        s = requests.session()

        s.headers.update({'User-Agent': 'Mozilla/5.0'})

        s.cookies.clear()

        r = s.get(BASE + SHOP_DIR + ALL_DIR + DEPARTMENT)

        item_hash = self._get_item_page(r.content)

        r = s.get(BASE + item_hash)

        item_ids = self._get_item_id(r.content)

        payload = {'style': item_ids['style'], 'size': item_ids['size'], 'commit': 'add+to+basket'}
        r = s.post(BASE + item_ids['link'], data=payload)

        r = s.get(BASE + SHOP_DIR + CART_DIR)

        for c in s.cookies :
            driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path, 'expiry': c.expires})

        driver.get("https://www.supremenewyork.com/checkout")
        field = driver.find_element_by_id("order_billing_name")
        field.send_keys("Marvin Himaer")
        field = driver.find_element_by_id("order_email")
        field.send_keys("marvinhimaer@rambler.ru")
        field = driver.find_element_by_id("order_tel")
        field.send_keys("89005553535")
        field = driver.find_element_by_id("bo")
        field.send_keys("lenina 1")
        field = driver.find_element_by_id("order_billing_city")
        field.send_keys("Dryutsk")
        field = Select(driver.find_element_by_id("order_billing_country"))
        field.select_by_visible_text("RUSSIA")
        field = driver.find_element_by_id("order_billing_zip")
        field.send_keys("214001")
        field = Select(driver.find_element_by_id("credit_card_type"))
        field.select_by_visible_text("Mastercard")
        field = driver.find_element_by_id("cnb")
        field.send_keys("5105105105105100")
        field = Select(driver.find_element_by_id("credit_card_month"))
        field.select_by_visible_text("01")
        field = Select(driver.find_element_by_id("credit_card_year"))
        field.select_by_visible_text("2020")
        field = driver.find_element_by_id("vval")
        field.send_keys("666")
        field = driver.find_element_by_id("order_terms")
        field.click()
        return

bot = SupBot()


bot.checkout("qwe")