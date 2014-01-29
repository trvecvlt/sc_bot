__author__ = 'maxim'

import requests
from bs4 import BeautifulSoup
import timing

#Set your own values for these constants
#TODO: move to interface
ITEM_SIZE = '8.5'
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

class KithBot:

    def _get_item_id(self, item_page_html):
        parsed_page = BeautifulSoup(item_page_html)
        for item in parsed_page.body.findAll('option'):
            if item.find(text=ITEM_SIZE):
                return item['value']
        return None

    def checkout(self, item_link):
        s = requests.session()

        r = s.get('http://shop.kithnyc.com/products/jswings2-0money')

        item_id = self._get_item_id(r.content)

        payload = {'id': item_id, 'add': 'Buy Now', 'quantity': '1'}
        r = s.post(CART_LINK+"/add", data=payload)

        payload = {'updates[{}]'.format(item_id): '1', 'checkout': 'Checkout'}
        r = s.post(CART_LINK, data=payload, verify=False)

        item_url = r.url

        r = s.get(item_url,verify=False)

        checkout_page_first = BeautifulSoup(r.content)
        aut_token = checkout_page_first.find('meta', attrs={'name':'csrf-token'})['content']

        payload = {'utf8':'%E2%9C%93','authenticity_token':aut_token,
                    'order[email]':ORDER_MAIL,'billing_address[first_name]':FIRST_NAME,
                    'billing_address[last_name]':LAST_NAME,'billing_address[company]':COMPANY_NAME,
                    'billing_address[address1]':ADDRESS_1,'billing_address[address2]':ADDRESS_2,
                    'billing_address[city]':CITY_NANE,'billing_address[zip]':ZIP,
                    'billing_address[country]':COUNTRY,'billing_address[province]':PROVINCE,
                    'billing_address[phon]':PHONE,'billing_is_shipping':'on',
                    'shipping_address[first_name]':FIRST_NAME,'shipping_address[last_name]':LAST_NAME,
                    'shipping_address[company]':COMPANY_NAME,'shipping_address[address1]':ADDRESS_1,
                    'shipping_address[address2]':ADDRESS_2,'shipping_address[city]':CITY_NANE,
                    'shipping_address[zip]':ZIP,'shipping_address[country]':COUNTRY,
                    'shipping_address[province]':PROVINCE,
                    'shipping_address[phone]':PHONE,'commit':'Continue+to+next+step'}

        print s.cookies
        r = s.post(item_url + "/create_order", data=payload, verify=False)
        print r.cookies

        checkout_url = r.url
        r = s.get(checkout_url)

        checkout_page_payment = BeautifulSoup(r.content)
        input_c = checkout_page_payment.body.find('input', attrs={'id':'c', 'name':'c'})['value']
        input_d = checkout_page_payment.body.find('input', attrs={'id':'d', 'name':'d'})['value']
        gateway = checkout_page_payment.body.find('input', attrs={'id':'direct-payment', 'name':'gateway'})['value']
        shopify_request_id = checkout_page_payment.body.find('input',
                                                        attrs={'id':'shopify_request_id',
                                                               'name':'shopify_request_id'})['value']
        gateway = checkout_page_payment.find('input', attrs={'id':'direct-payment','name':'gateway'})['value']
        payload = {'utf8':'%E2%9C%93','authenticity_token':aut_token, 'c':input_c, 'd':input_d,
                   'shopify_request_id':shopify_request_id,
                   'shipping_rate':'shopify-ups-ground-5-7-business-days-12.00',
                   'gateway':gateway,
                   'credit_card[first_name]':CREDIT_CARD_FIRST_NAME,'credit_card[last_name]':CREDIT_CARD_LAST_NAME,
                   'credit_card[number]':CREDIT_CARD_NUM,'credit_card[month]':CREDIT_CARD_MONTH,
                   'credit_card[year]':CREDIT_CARD_YEAR,'credit_card[verification_value]':CREDIT_CARD_CVV2,
                   'buyer_accepts_marketing':'false'
                   }

#        r = s.post('https://cselb.shopify.com/sessions', data= payload, verify = False)

 #       s.get(r.url)

        print (r.text)


from link_crawler import KithSpider
spider = KithSpider()
link = spider.search_link(None, None)
bot = KithBot()

bot.checkout(link)