#coding: utf8
import logging

from sqlalchemy import func

from controller_base import BaseController
from models import UserLogin, UserInfo, SpiderRecords


class IndexController(BaseController):
    "musicweb/index"
    def get(self):
        self.render("frontend/frontpage.html")

    def post(self):
        user_info = self.user_login()
        self.write(user_info)


class SongController(BaseController):
    "...song/([0-9]+)"
    def get(self):  # TODO
        self.render("frontend/songpage.html")


class SpaceController(BaseController):
    "...space/([0-9]+)"
    def get(self, space_id):
        self.render("frontend/userpage.html", space_id=space_id)

    def post(self, space_id):
        yourself = False
        user_login = self.user_login()
        if space_id == str(user_login["user_id"]):
            yourself = True
        user_info = self.user_info(space_id)
        user_info["space_id"] = space_id
        user_info["yourself"] = yourself
        self.write(user_info)


class ContributeController(BaseController):
    "...space/contributes/([0-9]+)"
    def get(self, space_id):
        self.render("frontend/contributes.html", space_id=space_id)

    def post(self, space_id):
        yourself = False
        user_login = self.user_login()
        if space_id == str(user_login["user_id"]):
            yourself = True
        user_info = self.user_info(space_id)
        user_info["space_id"] = space_id
        user_info["yourself"] = yourself
        self.write(user_info)


class ColumnController(BaseController):
    "...space/columns/([0-9]+)"
    def get(self, user_id):
        self.render("frontend/columns.html")


class ColumnEditController(BaseController):
    "...space/columns/([0-9]+)/edit"
    def get(self, user_id):
        self.render("frontend/column_edit.html")


class SettingController(BaseController):
    "...space/settings/([0-9]+)"
    def get(self, user_id):
        self.render("frontend/setting.html", user_id=user_id)

    def post(self, user_id):
        user_info = self.user_info(user_id)
        self.write(user_info)


class UserInfoChangeController(BaseController):
    "/api/userinfochange/([0-9]+)"
    def post(self, user_id):
        new_name = self.get_argument("username")
        new_desc = self.get_argument("desc")
        new_avatar = self.get_argument("avatar")
        ur = self.session.query(UserLogin).\
                filter(UserLogin._id==user_id).\
                first()
        ur.username = new_name
        ur.info[0].description = new_desc
        ur.info[0].avatar = new_avatar
        self.session.commit()
        self.write(dict(ret=0))


class SpiderIndexController(BaseController):
    "/api/spiderindex"
    def get(self):
        union = self.session.query(
                SpiderRecords.name, 
                SpiderRecords.author,
                func.group_concat(SpiderRecords.dsp_id),
                func.group_concat(SpiderRecords.link),
                func.group_concat(SpiderRecords.rank),
                func.count(SpiderRecords._id)).\
                group_by(SpiderRecords.name, SpiderRecords.author).\
                having(func.count(SpiderRecords._id)>1).\
                all()
        union_list = []
        for item in union:
            name = item[0]
            author = item[1]
            dsp_ids = item[2]
            links = item[3]
            ranks = item[4]
            dsp_ids = dsp_ids.split(',')
            links = links.split(',')
            ranks = ranks.split(',')
            comb = zip(dsp_ids, links, ranks)
            link_info = [{"dsp_id":com[0], "link":com[1], "rank":com[2]} for com in comb]
            union_dict = dict(name=name, author=author, link_info=link_info)
            union_list.append(union_dict)
        self.write(dict(union_list=union_list))

    def post(self):
        dsp_id = self.get_argument("dsp_id")
        spider_records = self.session.query(SpiderRecords).\
            filter(SpiderRecords.dsp_id==int(dsp_id)).\
            all()
        spider_list = []
        for record in spider_records:
            tmp_dict = dict(
                rank=record.rank,
                name=record.name,
                author=record.author,
                link=record.link,
                dsp_id=dsp_id
            )
            spider_list.append(tmp_dict)
        self.write(dict(spider_list=spider_list))
        
