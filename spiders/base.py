#coding:utf-8
import requests
from sqlalchemy.orm import sessionmaker
from scrapy.selector import Selector

from models.base import engine
from models.spiders import SpiderDsp
from models.get_session import orm_session


class BaseSpider(object):
    def __init__(self, dsp_id):
        self.dsp_id = dsp_id
        self.session = orm_session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
        }

    @property
    def get_link(self):
        link = self.session.query(SpiderDsp.link).\
                filter(SpiderDsp._id==self.dsp_id).\
                first()
        return link[0]

    def get_response(self):
        r = requests.get(self.get_link, headers=self.headers)
        return r

    def extract_all(self, xpath, text):
        content = Selector(text=text).xpath(xpath).extract()
        return content

