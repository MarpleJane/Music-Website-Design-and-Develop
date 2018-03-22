#coding:utf-8

"""
数据库模块
models:
    -- base: 基础类
    -- get_session: 获取session
    -- associations: 多对多的表
    -- knowledge: 科普相关表
    -- songs: 歌曲相关表
    -- spiders: 爬虫相关表
    -- users: 用户相关表
"""

from models.knowledge import *
from models.users import *
from models.songs import *
from models.spiders import *
from models.associations import *

from models.get_session import orm_session
