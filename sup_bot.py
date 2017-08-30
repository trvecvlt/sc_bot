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

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

DEPARTMENT = config.get('Item', 'Department')
ITEM = config.get('Item', 'Item')
COLOR = config.get('Item', 'Color')
ITEM_SIZE = config.get('Item', 'Size')

FULL_NAME = config.get('Buyer', 'Name')
ORDER_MAIL = config.get('Buyer', 'Mail')
PHONE = config.get('Buyer', 'Phone')
ADDRESS = config.get('Buyer', 'Address')
CITY = config.get('Buyer', 'City')
COUNTRY = config.get('Buyer', 'Country')
ZIP = config.get('Buyer', 'Zip')
ORDER_MAIL = config.get('Buyer', 'Mail')
CARD_TYPE = config.get('Buyer', 'CardType')
CREDIT_CARD_NUM = config.get('Buyer', 'CardNum')
CREDIT_CARD_MONTH = config.get('Buyer', 'Month')
CREDIT_CARD_YEAR = config.get('Buyer', 'Year')
CREDIT_CARD_CVV2 = config.get('Buyer', 'CVV')

class SupBot:


    def wait_start(self, runTime):
        from datetime import datetime, time
        from time import sleep
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

    def checkout(self):

        http_proxy  = "http://46.101.72.191:8118"


        proxyDict = {
                      "http"  : http_proxy
                    }

        from selenium import webdriver
        from selenium.webdriver.support.ui import Select
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("https://www.supremenewyork.com")

        try:
            self.wait_start(config.get('Item', 'start'))
        except ConfigParser.NoOptionError:
            pass

        s = requests.session()

        s.headers.update({'User-Agent': 'Chrome/60.0.3112.113'})

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
        field.send_keys(FULL_NAME)
        field = driver.find_element_by_id("order_email")
        field.send_keys(ORDER_MAIL)
        field = driver.find_element_by_id("order_tel")
        field.send_keys(PHONE)
        field = driver.find_element_by_id("bo")
        field.send_keys(ADDRESS)
        field = driver.find_element_by_id("order_billing_city")
        field.send_keys(CITY)
        field = Select(driver.find_element_by_id("order_billing_country"))
        field.select_by_visible_text(COUNTRY)
        field = driver.find_element_by_id("order_billing_zip")
        field.send_keys(ZIP)
        field = Select(driver.find_element_by_id("credit_card_type"))
        field.select_by_visible_text(CARD_TYPE)
        field = driver.find_element_by_id("cnb")
        field.send_keys(CREDIT_CARD_NUM)
        field = Select(driver.find_element_by_id("credit_card_month"))
        field.select_by_visible_text(CREDIT_CARD_MONTH)
        field = Select(driver.find_element_by_id("credit_card_year"))
        field.select_by_visible_text(CREDIT_CARD_YEAR)
        field = driver.find_element_by_id("vval")
        field.send_keys(CREDIT_CARD_CVV2)
        field = driver.find_element_by_id("order_terms")
        field.click()
        return


bot = SupBot()

bot.checkout()