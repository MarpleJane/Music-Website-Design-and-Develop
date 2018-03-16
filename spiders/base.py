#coding:utf-8
import requests
from sqlalchemy.orm import sessionmaker

from models.base import engine
from models.spiders import SpiderDsp
from models.get_session import orm_session


class BaseSpider(object):
    def __init__(self, dsp_id):
        self.dsp_id = dsp_id
        self.session = orm_session()

    @property
    def get_link(self):
        link = self.session.query(SpiderDsp.link).\
                filter(SpiderDsp._id==self.dsp_id).\
                first()
        return link

    def get_target(self):
        pass
        return
