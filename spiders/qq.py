#coding: utf-8
import json
from datetime import datetime
from datetime import timedelta

import requests

from models import SpiderDsp
from models import SpiderRecords
from spiders.base import BaseSpider


class QQSpider(BaseSpider):
    URI = "fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date={}&topid=4&type=top&song_begin=0&song_num=100&g_tk=763535586&loginUin=2403635410&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
    PATTERN = "https://y.qq.com/n/yqq/song/{}.html"

    def __init__(self, dsp_id):
        super(QQSpider, self).__init__(dsp_id)
        #self.headers["user-agent"] = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
        #del self.headers["User-Agent"]
        self.headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

    def get_response(self):
        d = timedelta(days=2)
        date = (datetime.now().date() - d).isoformat()
        #date = datetime.now().date().isoformat()
        url = self.get_link + self.URI.format(date)
        print(url)
        r = requests.get(url, headers=self.headers)
        return r

    def parse(self):
        response = self.get_response()
        print("[Status Code]: ", response.status_code)
        if response.status_code >= 400:
            raise Exception

        load = json.loads(response.text)
        code = load["code"]
        if code != 0:
            raise Exception

        song_list = load["songlist"]

        rank = 0
        for song in song_list:
            data = song["data"]
            rank += 1
            name = data["songorig"]
            author = [ au["name"] for au in data["singer"] ]
            author = "|".join(author)
            song_id = data["songmid"]
            url = self.PATTERN.format(song_id)
            record = SpiderRecords(
                dsp_id=self.dsp_id,
                rank=rank,
                name=name,
                author=author,
                link=url
            )
            self.session.add(record)
        self.session.commit()
