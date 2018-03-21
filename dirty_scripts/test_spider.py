#coding: utf-8
#from spiders import NeteaseSpider
#from spiders import QQSpider
from spiders import KugouSpider


if __name__ == "__main__":
    #netease = NeteaseSpider(1)
    #netease.parse()

    #qq = QQSpider(2)
    #qq.parse()

    kugou = KugouSpider(3)
    kugou.parse()
