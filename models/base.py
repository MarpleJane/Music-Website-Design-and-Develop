#coding: utf-8

import re

import pymysql
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import create_engine


engine = create_engine("mysql+pymysql://root:shellingford@127.0.0.1:3306/musicwebsite?charset=utf8")


def _camel_case_2_snake_case(name):
    tmp = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', tmp).lower()


@as_declarative()
class ORMBase(object):

    @declared_attr
    def __tablename__(cls):
        return _camel_case_2_snake_case(cls.__name__)
