# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述：创建数据库和表文件
# 主要模块： 1. 创建数据库
#          2. 创建表文件
#
# 作者: 方成
# 单位： 云南大学信息学院
# 生成日期：2020-11-03
# ----------------------------------------------------------------------------- #
import config
import logging
import time
from utils import RESULT_FAILED, RESULT_OK, RESULT_ERROR
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from utils import get_session

# 生成ORM基类
Base = declarative_base()


class User(Base):
    """
    新建用户信息表
    """
    __tablename__ = "user_info"                                        # 表名
    ID = Column(Integer, primary_key=True, autoincrement=True)         # 自增编号
    OPEN_ID = Column(String(64))                                       # 微信用户的openid
    NICK_NAME = Column(String(64))                                     # 微信用户昵称
    GENDER = Column(String(32))                                        # 性别
    PHONE = Column(String(48))
    DATE_TIME = Column(DateTime, nullable=False)

    def __init__(self, user_id, nick_name, gender, phone, date_time):
        self.OPEN_ID = user_id
        self.NICK_NAME = nick_name
        self.GENDER = gender
        self.PHONE = phone
        self.DATE_TIME = date_time


def create_table():
    """
    新建一个user_info表文件
    """
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL, encoding="utf-8")
        # 执行创建表结构
        Base.metadata.create_all(engine)
        logging.info('create table: user_info 成功！')
        return RESULT_OK
    except Exception as e:
        logging.critical('create table: user_info 失败！ {0}'.format(e))
        return RESULT_FAILED


def drop_table():
    """
    删除user_info表文件
    """
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL, encoding="utf-8")
        # 执行创建表结构
        Base.metadata.drop_all(engine)
        logging.info('drop table: user_info 成功！')
        return RESULT_OK
    except Exception as e:
        logging.critical('drop table: user_info 失败！ {0}'.format(e))
        return RESULT_FAILED


def insert_data(**kwargs):
    """
    添加一个或多个用户信息
    :param kwargs: 用户信息，输入格式[{'user_id':user_id, 'nick_name':nick_name, 'phone':phone}, ...]
    :return:
    """
    session = None
    try:
        session = get_session()
        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        nick_name = '' if kwargs['nick_name'] is None else kwargs['nick_name']
        gender = '' if kwargs['gender'] is None else kwargs['gender']
        phone = '' if kwargs['phone'] is None else kwargs['phone']

        new_info = User(user_id=kwargs['user_id'],
                        nick_name=nick_name,
                        gender=gender,
                        phone=phone,
                        date_time=_time)

        session.add(new_info)
        # 提交到数据库
        session.commit()
        logging.info('OK : users.py--->insert_data(), 成功添加一条用户信息')
        return RESULT_OK
    except Exception as e:
        # 出错时，回滚一下清楚数据
        session.rollback()
        logging.critical('Error : users.py--->insert_data() : {0}'.format(e))
        return RESULT_FAILED
    finally:
        # 关闭session
        session.close()


def query_data(**kwargs):
    """
    根据输入的用户ID查询用户信息
    :param kwargs: {'user_id': user_id}
    :return:
    """
    session = None
    try:
        session = get_session()
        result = session.query(User).filter(User.OPEN_ID == kwargs['user_id']).all()
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : users.py--->query_data(), 成功查询到用户信息')
        results, res = [], {}
        for r in result:
            res['NICK_NAME'] = r.NICK_NAME
            res['PHONE'] = r.PHONE
            res['GENDER'] = r.GENDER
            results.append(res)

        return results
    except Exception as e:
        logging.critical('Error : users.py--->query_data() : {0}'.format(e))
        return []
    finally:
        # 关闭session
        session.close()


def query_all():
    """
    根据输入的用户ID查询用户信息
    :param :
    :return:
    """
    session = None
    try:
        session = get_session()
        result = session.query(User).all()
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : users.py--->query_data(), 成功查询到用户信息')
        results = []
        for r in result:
            res = {'OPEN_ID': r.OPEN_ID, 'NICK_NAME': r.NICK_NAME, 'PHONE': r.PHONE, 'GENDER': r.GENDER}
            results.append(res)
        return results
    except Exception as e:
        logging.critical('Error : users.py--->query_data() : {0}'.format(e))
        return []
    finally:
        session.close()


if __name__ == '__main__':
    # drop_table()
    # create_table()
    users = {'user_id': '0123', 'nick_name': 'fC', 'gender': 0, 'phone': '123'}
    # print([use.GENDER for use in ret])
