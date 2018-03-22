#coding: utf-8
import re

from scrapy.selector import Selector

from models import SpiderRecords
from spiders.base import BaseSpider


class KugouSpider(BaseSpider):
    def __init__(self, dsp_id):
        super(KugouSpider, self).__init__(dsp_id)
        self.headers["Host"] = "www.kugou.com"

    def parse(self):
        response = self.get_response()
        if response.status_code >= 400:
            raise Exception

        xpath_a = "//div[@id='rankWrap']//ul/li/a[@class='pc_temp_songname']"
        el_a = self.extract_all(xpath_a, response.text)

        rank = 0
        for a in el_a:
            rank += 1
            url = self.extract_all("//@href", a)[0]
            combine = self.extract_all("//@title", a)[0]
            author, name = combine.split(" - ")
            author = "|".join(author.split("、"))
            #ch_bracket = name.index(u"【")
            ch_bracket = name.find("\u3010")
            if ch_bracket > 0:
                name = name[:ch_bracket]
            record = SpiderRecords(
                dsp_id=self.dsp_id,
                rank=rank,
                name=name,
                author=author,
                link=url
            )
            self.session.add(record)
        self.session.commit()
