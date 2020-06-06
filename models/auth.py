from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, ForeignKey

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.db import Base, session


class BaseModels:
    is_delete = Column(Boolean, default=False)  # 逻辑删除
    update_time = Column(DateTime, default=datetime.now)  # 修改
    create_time = Column(DateTime, default=datetime.now)  # 创建


class User(Base, BaseModels):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    activation = Column(Boolean, default=False)     # 激活
    email = Column(String(100))
    phone = Column(String(30))

    @classmethod
    def add_user(cls, username, password, **kwargs):
        user = User(username=username, password=password, **kwargs)
        session.add(user)
        session.commit()
        session.close()

    @classmethod
    def check_username(cls, username):
        return session.query(cls).filter_by(username=username).first()

    def __repr__(self):
        return "User:username=%s,password=%s" % (self.username, self.password)


# 分类表
class PostType(Base, BaseModels):
    __tablename__ = 'posttype'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200))


class Post(Base, BaseModels):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    content = Column(String(500))
    image_url = Column(String(300))
    thumbnail_url = Column(String(300))     # 缩略图

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="posts", uselist=False, cascade="all")

    posttype_id = Column(Integer, ForeignKey("posttype.id"))
    posttype = relationship("PostType", backref="p_type", uselist=False, cascade="all")

    def __repr__(self):
        return "Post:title=%s" % self.title

    @classmethod
    def add_post(cls, title, content, image_url, thumbnail_url, username, posttype_id):
        user = User.check_username(username)    # 返回user实例
        post = Post(title=title, content=content, image_url=image_url, thumbnail_url=thumbnail_url, user_id=user.id, posttype_id=posttype_id)
        session.add(post)
        session.commit()
        session.close()


# 评论表
class Comment(Base, BaseModels):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    reply_id = Column(Integer, ForeignKey("comment.id"))
    up = Column(Integer)
    down = Column(Integer)
    content = Column(String(200))






# 图片实例.user===>拿到对应的user实例
# 用户实例.posts===>拿到对应的图片实例