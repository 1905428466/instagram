import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    """
    首页， 用户上传图片的展示
    """
    def get(self):
        return self.write("首页")


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
        return self.write("详情页")