import tornado.ioloop
import tornado.web  #web应用api
import tornado.options
from tornado.options import define, options

from handlers.main import IndexHandler, ExploreHandler, PostHandler
from handlers.users import RegisterHandler, LoginHandler

define("port", default="8888", help="Listening port", type=int)


class Application(tornado.web.Application): #tornado配置，比如静态文件
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/expore", ExploreHandler),
            (r"/post/(?P<post_id>[0-9]+)", PostHandler),
            (r"/register", RegisterHandler),
            (r"/login", LoginHandler),
        ]
        settings = dict(
            debug=True,
            template_path="templates"  # 配置模板路径
        )

        super().__init__(handlers, **settings)


if __name__ == "__main__":  #只有在当前文件运行的时候才会执行
    tornado.options.parse_command_line()    # 命令行
    application = Application()  # 实例化
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start() #开启tornado服务

