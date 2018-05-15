#coding: utf8
import logging
import os
import json

from sqlalchemy import func

from controller_base import BaseController
from models import UserLogin, UserInfo, SpiderRecords, Columns, Songs, Comments, Carousel


DOMAIN = "http://192.168.31.10/"


def get_obj_attrs(attrs, obj):
    return {attr: getattr(obj, attr) for attr in attrs}


def get_attrs(attrs, obj_list):
    return [{attr: getattr(obj, attr) for attr in attrs} for obj in obj_list]


class IndexController(BaseController):
    "musicweb/index"
    def get(self):
        self.render("frontend/frontpage.html")

    def post(self):
        user_info = self.user_login()
        self.write(user_info)


class SongController(BaseController):
    "...song/([0-9]+)"
    def get(self, song_id):  # TODO
        user = self.current_user("user_id")
        if not user:
            user = 0
        else:
            user = 1
        song_info = self.session.query(Songs).\
            filter(Songs._id==int(song_id)).\
            first()
        attrs = ["_id", "name", "cover_path", "store_path", "uploader_name", "uploader_url"]
        uploader = self.session.query(UserLogin).\
            filter(UserLogin._id==song_info.uploader).\
            first()
        self.render("frontend/songpage.html",
            name=song_info.name,
            cover_path=song_info.cover_path,
            file_path=song_info.file_path,
            artist=song_info.author,
            uploader=uploader.account,
            uploader_id=uploader._id,
            desc=song_info.description,
            user=user,
            song_id=int(song_id)
        )

    def post(self, song_id):
        user = self.user_login()
        self.write(user)


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
    def get(self, space_id):
        self.render("frontend/columns.html", space_id=space_id)

    def post(self, space_id):
        yourself = False
        user_login = self.user_login()
        if space_id == str(user_login["user_id"]):
            yourself = True
        user_info = self.user_info(space_id)
        user_info["space_id"] = space_id
        user_info["yourself"] = yourself
        self.write(user_info)


class ColumnEditController(BaseController):
    "...space/columns/([0-9]+)/edit"
    def get(self, user_id):
        self.render("frontend/column_edit.html", user_id=user_id)

    def post(self, user_id):
        column_name = self.get_argument("name")
        uri = self.get_argument("uri")
        url = DOMAIN + uri
        new_column = Columns(name=column_name, author_id=user_id, store_url=url)
        self.session.add(new_column)
        self.session.commit()
        self.write(dict(ret=0))


class ColumnContentController(BaseController):
    "...space/column/([0-9]+)"
    def get(self, column_id):
        self.render("frontend/column_content.html", column_id=column_id)

    def post(self, column_id):
        column = self.session.query(Columns).\
                filter(Columns._id==column_id).\
                first()
        attrs = ["_id", "name", "author_id", "store_url"]
        column_info = get_obj_attrs(attrs, column)
        user_info = self.user_info(column_info["author_id"])
        column_info["author"] = user_info["username"]
        self.write(column_info)


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
        current_user = self.current_user("user_id")
        current_user = int(current_user) if current_user else 0
        new_name = self.get_argument("username")
        new_desc = self.get_argument("desc")
        new_avatar = self.get_argument("avatar")
        if new_avatar:
            new_avatar = DOMAIN + new_avatar
        if current_user:
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
        

class ImportController(BaseController):
    """/api/importsong"""
    def post(self):
        music_path = self.get_argument("music_path")
        cover_path = self.get_argument("cover_path")
        music_type = self.get_argument("music_type")
        song_name = self.get_argument("song_name")
        origin = self.get_argument("origin")
        desc = self.get_argument("desc")
        artist = self.get_argument("artist")
        uploader = self.current_user("user_id")
        song = Songs(
            uploader=int(uploader),
            name=song_name,
            cover_path=DOMAIN + cover_path,
            author=artist,
            file_path=DOMAIN + music_path,
            description=desc,
            type_id=music_type,
            origin=origin,
        )
        self.session.add(song)
        self.session.commit()
        self.write(dict(ret=0))


class ColumnIndexController(BaseController):
    """/api/allcolumns"""
    def get(self):
        all_columns = self.session.query(Columns).\
            order_by(Columns.created_time.desc()).\
            all()
        attrs = ["_id", "name", "author_id", "author", "url"]
        columns = get_attrs(attrs, all_columns)
        self.write(dict(columns=columns))


class ColumnSpaceController(BaseController):
    """/api/columnspace/([0-9]+)"""
    def get(self, space_id):
        space_id = int(space_id)
        space_columns = self.session.query(Columns).\
            filter(Columns.author_id==space_id).\
            order_by(Columns.created_time.desc()).\
            all()
        attrs = ["_id", "name", "author_id", "author", "url"]
        columns = get_attrs(attrs, space_columns)
        self.write(dict(columns=columns))


class SongIndexController(BaseController):
    """/api/songindex/?"""
    attrs = ["_id", "name", "url", "cover_path", "song_type", "type_id", "uploader_name", "origin_type"]

    def newly(self):
        new_upload = self.trail_pass().\
            order_by(Songs.created_time.desc()).\
            slice(0, 5)
        return get_attrs(self.attrs, new_upload)

    def diy(self):
        diy = self.trail_pass().\
            filter(Songs.origin==1).\
            order_by(Songs.created_time.desc()).\
            slice(0, 5)
        return get_attrs(self.attrs, diy)

    def nodiy(self):
        nodiy = self.trail_pass().\
            filter(Songs.origin==2).\
            order_by(Songs.created_time.desc()).\
            slice(0, 5)
        return get_attrs(self.attrs, nodiy)
    
    def query_result(self):
        query = self.get_argument("query")
        query = int(query)
        result = []
        result1 = self.newly()
        result2 = self.diy()
        result3 = self.nodiy()
        if query == 1:
            result.append(result1)
        elif query == 2:
            result.append(result2)
        elif query == 3:
            result.append(result1)
            result.append(result2)
        elif query == 4:
            result.append(result4)
        elif query == 5:
            result.append(result1)
            result.append(result3)
        elif query == 6:
            result.append(result2)
            result.append(result3)
        elif query == 7:
            result.append(result1)
            result.append(result2)
            result.append(result3)
        return result

    def get(self):
        results = self.query_result()
        self.write(dict(results=results))

    def origin(self, current, page_size):
        start = (current - 1) * page_size
        end = start + page_size
        total = self.trail_pass().\
            filter(Songs.origin==1).\
            count()
        if end > total:
            end = total
        origin_records = self.trail_pass().\
            order_by(Songs.created_time.desc()).\
            slice(start, end)
        origin_list = get_attrs(self.attrs, origin_records)
        return [origin_list, total]

    def all_songs(self):
        songs = self.trail_pass().all()
        song_list = get_attrs(self.attrs, songs)
        return song_list

    def post(self):
        query = self.get_argument("query")
        query = int(query)
        if query == 2:
            current = self.get_argument("current")
            current = int(current)
            page_size = self.get_argument("pageSize")
            page_size = int(page_size)
            origin_list, total = self.origin(current, page_size)
            self.write(dict(origin_list=origin_list, total=total))
        if query == 8:
            song_list = self.all_songs()
            self.write(dict(song_list=song_list))


class SongSpaceController(BaseController):
    """/api/songspace"""
    attrs = ["_id", "name", "url", "cover_path", "song_type", "type_id", "uploader_name", "origin_type"]

    def space_trail(self, current, page_size, space_id):
        start = (current - 1) * page_size
        end = start + page_size
        total = self.trail_pass().\
            filter(Songs.uploader==space_id).\
            count()
        if end > total:
            end = total
        space_records = self.trail_pass().\
            filter(Songs.uploader==space_id).\
            order_by(Songs.created_time.desc()).\
            slice(start, end)
        space_list = get_attrs(self.attrs, space_records)
        return [space_list, total]

    def post(self):
        space_id = self.get_argument("space_id")
        space_id = int(space_id)
        current = self.get_argument("current")
        current = int(current)
        page_size = self.get_argument("pageSize")
        page_size = int(page_size)
        space_list, total = self.space_trail(current, page_size, space_id)
        self.write(dict(space_list=space_list, total=total))


class SongTrailController(BaseController):
    """/api/songtrail"""
    attrs = ["_id", "name", "flag_name"]

    def trail_list(self, current, page_size):
        current_user = self.current_user("user_id")
        current_user = int(current_user)
        start = (current - 1) * page_size
        end = start + page_size
        total = self.session.query(Songs).\
            filter(Songs.uploader==current_user).\
            count()
        if end > total:
            end = total
        trail_records = self.session.query(Songs).\
            filter(Songs.uploader==current_user).\
            order_by(Songs.created_time.desc()).\
            all()
        trail_list = get_attrs(self.attrs, trail_records)
        return [trail_list, total]

    def post(self):
        current = self.get_argument("current")
        current = int(current)
        page_size = self.get_argument("pageSize")
        page_size = int(page_size)
        trail_list, total = self.trail_list(current, page_size)
        self.write(dict(trail_list=trail_list, total=total))


class CommentController(BaseController):
    """/api/comments?"""
    attrs = ["content", "author_id", "username", "avatar"]

    def get(self):
        song_id = self.get_argument("song_id")
        song_id = int(song_id)
        comments = self.session.query(Comments).\
            filter(Comments.song_id==song_id).\
            all()
        comment_list = get_attrs(self.attrs, comments)
        self.write(dict(comment_list=comment_list))

    def post(self):
        song_id = self.get_argument("song_id")
        song_id = int(song_id)
        user_id = self.get_argument("user_id")
        user_id = int(user_id)
        msg = self.get_argument("msg")
        comment = Comments(content=msg, author_id=user_id, song_id=song_id)
        self.session.add(comment)
        self.session.commit()
        self.write(dict(ret=0))


class CarouselController(BaseController):
    """/api/carousel"""
    attrs = ["url", "target"]

    def get(self):
        carousels = self.session.query(Carousel).all()
        carousel_list = get_attrs(self.attrs, carousels)
        self.write(dict(carousel_list=carousel_list))

    def post(self):
        target = self.get_argument("target")
        car_id = self.get_argument("car_id")
        car_id = int(car_id)
        url = self.get_argument("url")
        car = self.session.query(Carousel).filter(Carousel._id==car_id).first()
        car.url = DOMAIN + url
        car.target = target
        self.session.commit()
        self.write(dict(target=target, url=url))
