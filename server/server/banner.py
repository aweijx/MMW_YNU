# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述：创建轮播图的数据库和表文件
# 主要模块： 1. 创建数据库
#          2. 创建表文件
#
# 作者: 方成
# 单位： 云南大学信息学院
# 生成日期：2020-10-27
# ----------------------------------------------------------------------------- #
import config
import logging
import time
from utils import RESULT_FAILED, RESULT_OK, RESULT_ERROR, get_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

# 生成ORM基类
Base = declarative_base()


class Banner(Base):
    """
    新建伦播图信息表
    """
    __tablename__ = "banner_info"                                      # 表名
    ID = Column(Integer, primary_key=True, autoincrement=True)         # 自增编号
    IMG_URL = Column(String(320))                                      # 轮播图的URL
    DATE_TIME = Column(DateTime, nullable=False)

    def __init__(self, img_url, date_time):
        self.IMG_URL = img_url
        self.DATE_TIME = date_time


def create_table():
    """
    新建一个swiper_images_info表文件
    """
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL, encoding="utf-8")
        # 判断数据库连接返回值是否为空
        if engine is None:
            logging.error('FAILD: banner.py--->create_table() 生成数据库连接失败！')
            return RESULT_FAILED

        # 执行创建表结构
        Base.metadata.create_all(engine)
        logging.info('OK: banner.py--->create_table()  成功！')
        return RESULT_OK
    except Exception as e:
        logging.critical('ERROR: banner.py--->create_table() 失败！ {0}'.format(e))
        return RESULT_ERROR


def drop_table():
    """
    删除user_info表文件
    """
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL, encoding="utf-8")
        # 判断数据库连接返回值是否为空
        if engine is None:
            logging.error('FAILED: banner.py--->drop_table() 生成数据库连接失败！')
            return RESULT_FAILED

        # 执行创建表结构
        Base.metadata.drop_all(engine)
        logging.info('OK: banner.py--->drop_table()  成功')
        return RESULT_OK
    except Exception as e:
        logging.critical('ERROR: banner.py--->drop_table() 失败！ {}'.format(e))
        return RESULT_ERROR


def insert_data(**kwargs):
    """
    添加一个或多个论波图
    :param kwargs: 输入格式{'img_url':img_url}
    :return:
    """
    session = None
    try:
        session = get_session()
        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        new_banner = Banner(img_url=kwargs['img_url'], date_time=_time)
        # 全部添加到session
        session.add(new_banner)
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : banner.py--->insert_data() 成功添加一条用户信息')
        return RESULT_OK
    except Exception as e:
        # 出错时，回滚一下
        session.rollback()
        logging.critical('Error : banner.py--->insert_data() 失败: {0}'.format(e))
        return RESULT_ERROR
    finally:
        session.close()


def del_data(**kwargs):
    """
    删除一个轮播图
    :param kwargs: {'img_url': img_url}
    :return:
    """
    session = None
    try:
        session = get_session()
        session.query(Banner).filter(Banner.IMG_URL == kwargs['img_url']).delete()
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : banner.py--->del_data(), 成功')
        return RESULT_OK
    except Exception as e:
        logging.critical('Error : banner.py--->del_data() 失败：{}'.format(e))
        return []
    finally:
        session.close()


def query_data():
    """
    根据输入的用户ID查询用户信息
    :param
    :return:
    """
    # condition: {'url_size': url_size}
    # if not isinstance(condition, dict):
    #    logging.error('Error : banner.py--->query_data() 为空或类型不正确!')
    #    return []

    # if condition['url_size'] is None or '' == condition['url_size']:
    #    logging.error('Error : banner.py--->query_data() 为空或类型不正确!')
    #    return []
    session = None
    try:
        session = get_session()
        result = session.query(Banner.IMG_URL).all()
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : banner.py--->query_data(), 成功')
        results = [{'IMG_URL': _res.IMG_URL} for _res in result]
        return results
    except Exception as e:
        logging.critical('Error : banner.py--->query_data() 失败: {}'.format(e))
        return []
    finally:
        session.close()


if __name__ == '__main__':
    # drop_table()
    create_table()
