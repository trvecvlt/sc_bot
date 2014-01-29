__author__ = 'maxim'

import requests
import timing
import re
import hashlib
import time
from twython import TwythonStreamer
from abc import ABCMeta, abstractmethod, abstractproperty


class LinkCrawler(object):
    __metaclass__=ABCMeta

    def search_link(self, searchMask, searchLink):
        """Basic method for all classes.
        Takes link to search and some search parameter
        and returns found url


        :rtype : string
        :param searchMask: (required) params for search(keywords, regular expression and etc.)
        :param searchLink: (required) where item should be searched. It could be an url, twitter id and etc.
        """


class KithSpider(LinkCrawler):

    KITH_SITEMAP = "http://shop.kithnyc.com/sitemap_products_1.xml"

    def search_link(self, searchMask, searchLink=KITH_SITEMAP):
        """


        :rtype : string
        :param searchMask: (required) regular expression for item
        :param searchLink: (optional) sitemap link
        :return: item url
        """

        old_xml_hash = hashlib.md5("")
        while True:
            try:
                r = requests.get(searchLink)
            except requests.exceptions.ConnectionError:
                print "ConnectionError"
                time.sleep(10)
                continue
            xml_text = r.content
            if old_xml_hash.hexdigest() == hashlib.md5(xml_text).hexdigest():
                time.sleep(2)
                continue
            for url in re.findall(pattern='<url>[\s\S]*?</url>', string= xml_text):
                img_title = re.search(pattern='<image:title>(?P<Image_Title>[\s\S]*?)</image:title>', string= url)
                if img_title is not None and \
                        re.match(pattern=r'(?=.*\bPuma\b)(?=.*\bRonnie\sFieg|RF\b)(?=.*\bCoat\sOf\sArms|COA\b).*',
                                 string=img_title.group('Image_Title'), flags=re.IGNORECASE):
                    res = re.search(pattern='<loc>(?P<Item_Link>[\s\S]*?)</loc>', string=url).group('Item_Link')
                    return res
            print "NotFound"
            old_xml_hash = hashlib.md5(xml_text)


class LinkSearchStreamer(TwythonStreamer):

    LINK_REGEX_STRING = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    def __init__(self, app_key, app_secret, oauth_token, oauth_token_secret,
                 search_mask):
        """Wrapper around twython streaming api

        :param app_key: (required) Your applications key
        :param app_secret: (required) Your applications secret key
        :param oauth_token: (required) Used with oauth_token_secret to make
                            authenticated calls
        :param oauth_token_secret: (required) Used with oauth_token to make
                                   authenticated calls
        :param search_mask: (required)
        """
        super(LinkSearchStreamer, self).__init__(app_key, app_secret, oauth_token, oauth_token_secret)
        self.search_mask = search_mask

    def on_success(self, data):
        if 'text' in data:
            match = re.search(pattern = self.search_mask, string = data['text'].encode('utf-8'))
            if match:
                self.links = re.findall(LINK_REGEX_STRING, data['text'].encode('utf-8'))
                self.disconnect()
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code


class TwitterCrawler(LinkCrawler):

    def _authorize(self):
        """ Authorize crawler app on twitter

             Sets authorization keys for OAuth1

        """

        #TODO: move key values to separate file and read from there

        self.app_key = 'MeFVT0nsARESWZRcWQP4Ng'
        self.app_secret = 'mtRZT0ar6oaZT6MPfv62EPUn07170VgNyj7svpl1Ks'

        #twitter = Twython(APP_KEY, APP_SECRET)
        #auth = twitter.get_authentication_tokens(callback_url='oob')

        self.oauth_token = '2296614344-IJZyK9pkAWJYWPiBsb6PL4UuRqDlXyjj9HxHSHU'#auth['oauth_token']
        self.oauth_token_secret = 'WeNY6d39VM4dVjrmjAqB5zodlfzNx3Y3SAbBRpu4bebXW'#auth['oauth_token_secret']

    def __init__(self):
        self.authorize()

    def search_link(self, search_mask, search_links):
        """ Crawl twitter accounts for link to item in store

        :param search_mask: (required) should contain regex with mask,
                            that will be applied to all cathced tweets
        :param search_links: (required) should contain user ids for
                            accounts, which will be watched for link

        Method returns url string for item if it's found
        """

        stream = LinkSearchStreamer(self.app_key, self.app_secret,
                            self.oauth_token, self.oauth_token_secret, search_mask)
        stream.statuses.filter(follow=self.search_links)
        links = stream.links
        return links
