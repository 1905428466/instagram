import os
import tornado.web
from pycket.session import SessionMixin
from models.auth import Post
from models.db import session


class BaseHandler(SessionMixin, tornado.web.RequestHandler):
    def get_current_user(self):
        return self.session.get("user")


class IndexHandler(tornado.web.RequestHandler):
    """
    首页， 用户上传图片的展示
    """
    def get(self):
        posts = session.query(Post).all()
        return self.render("index.html", posts=posts)


class ExploreHandler(tornado.web.RequestHandler):
    """
    最近上传的图片页面
    """
    def get(self):
        return self.write("发现或最近上传的图片页面")


class PostHandler(tornado.web.RequestHandler):
    """
    单个图片的详情页面
    """
    def get(self, post_id):
        return self.render("single.html")


class UpdateHandler(BaseHandler):
    """
    图片上传
    """
    @tornado.web.authenticated
    def get(self):
        return self.render("update.html")

    @tornado.web.authenticated
    def post(self):
        upload_path = "statics/upload"  # 配置上传的路径
        file_metas = self.request.files.get("image_file", [])    # 获取图片

        # 写入文件
        for meta in file_metas:
            file_name = meta.get("filename")    # 获取文件名
            file_path = os.path.join(upload_path, file_name)
            with open(file_path, "wb") as up:
                up.write(meta.get("body"))  # 写入内容

            # 入库
            Post.add_post("upload/%s" % file_name, self.current_user)
            return self.write("上传成功")