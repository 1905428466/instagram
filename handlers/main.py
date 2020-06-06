import os
import uuid
import time
import tornado.web
from tornado import gen
from PIL import Image
from pycket.session import SessionMixin
from models.auth import Post, PostType
from models.db import session


class BaseHandler(SessionMixin, tornado.web.RequestHandler):
    def get_current_user(self):
        return self.session.get("user")

@gen.coroutine
def asy_update():
    # time.sleep(5)
    # yield gen.sleep(5)
    posttype_all = session.query(PostType).all()
    raise gen.Return(posttype_all)
    # return posttype_all

class IndexHandler(BaseHandler):
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
        posts = session.query(Post).get(post_id)
        type_all = session.query(PostType).all()
        if not posts:
            return self.write_error(404)
        return self.render("single.html", posts=posts, type_all=type_all)


class UpdateHandler(BaseHandler):
    """
    图片上传
    """
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        posttype_all = yield asy_update()
        return self.render("update.html", posttype_all=posttype_all)

    @tornado.web.authenticated
    def post(self):
        title = self.get_argument("title", "")
        content = self.get_argument("content", "")

        upload_path = "statics/upload"  # 配置上传的路径
        file_metas = self.request.files.get("image_file", [])    # 获取图片

        # 写入文件
        for meta in file_metas:
            image_type = meta.get("filename").split(".")[-1]    # 获取后缀名
            file_name = str(uuid.uuid1()) + "." + image_type    # 构造文件名
            file_path = os.path.join(upload_path, file_name)
            with open(file_path, "wb") as up:
                up.write(meta.get("body"))  # 写入内容

            # 缩略图
            im = Image.open(file_path)  # 打开图片
            im.thumbnail((259.69, 270))
            thumbnail_url = "upload/thumbnail/%s" % file_name
            im.save("statics/%s" % thumbnail_url, image_type if image_type == "png" else "JPEG")


            # 入库
            Post.add_post(title, content, "upload/%s" % file_name, thumbnail_url, self.current_user, 2)
        return self.write("上传成功")