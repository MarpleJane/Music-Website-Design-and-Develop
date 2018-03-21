#coding: utf-8
import json

from scrapy.selector import Selector

from models import SpiderDsp
from models import SpiderRecords
from spiders.base import BaseSpider


class NeteaseSpider(BaseSpider):
    HOST = "music.163.com"
    PATTERN = HOST + "song?id={}"

    def __init__(self, dsp_id):
        super(NeteaseSpider, self).__init__(dsp_id)
        self.headers["Host"] = self.HOST

    def parse(self):
        response = self.get_response()
        if response.status_code >= 400:
            raise Exception

        #xpath_uri = "//div[@id='song-list-pre-cache']//ul[@class='f-hide']//li//a/@href"
        #xpath_title = "//div[@id='song-list-pre-cache']//ul[@class='f-hide']//li//a/text()"
        xpath_textarea = "//textarea/text()"
        list_text = Selector(text=response.text).xpath(xpath_textarea).extract_first()
        lists = json.loads(list_text)
        
        rank = 0
        for lt in lists:
            rank += 1
            song_id = lt["id"]
            name = lt["name"]
            author = [ au["name"] for au in lt["artists"] ]
            author = "|".join(author)
            url = self.PATTERN.format(song_id)
            record = SpiderRecords(
                dsp_id=self.dsp_id,
                rank=rank,
                name=name,
                author=author,
                link=url,
            )
            self.session.add(record)
        self.session.commit()
