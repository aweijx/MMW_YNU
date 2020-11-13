# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述： 发布招领信息，以及查询和状态更新 等信息
# 主要函数：
#         1.  create_table
#         2.  drop_table
#         3.  insert_data
#         4.  del_data
#         5.  update_status
#         6.  update_seen_cnt     .
#         7.  update_forward_cnt
#         8.  query_by_seen
#         9.  query_by_forward
#         10. query_by_name        .
#         11. query_by_class       .
#         12. query_by_found_id    .
#         13. query_by_user_id     .
#         14. query_by_date_before .
#         15. query_by_date_after  .
#         16. query_by_date_between  .
#
#
# 作者: 方成
# 单位： 云南大学信息学院
# 生成日期：2020-11-05
# ----------------------------------------------------------------------------- #
import config
import logging
import time
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, and_
from utils import RESULT_ERROR, RESULT_OK, RESULT_FAILED, gen_object_id, get_session

# 生成ORM基类
Base = declarative_base()


class Found(Base):
    """
    新建招领信息表
    """
    __tablename__ = "found_info"                                       # 表名
    ID = Column(Integer, primary_key=True, autoincrement=True)         # 自增编号
    OPEN_ID = Column(String(96), nullable=False)                       # 微信用户的openid
    OBJECT_ID = Column(String(96), nullable=False, unique=True)        # 丢失物的ID
    OBJECT_NAME = Column(String(96))                                   # 物件的昵称
    OBJECT_CLASS = Column(String(96), nullable=False)                  # 物品类别
    OBJECT_STATUS = Column(String(96), nullable=False)                 # 物品当前的状态
    IMG_URL = Column(String(2048))                                     # 物品图像
    MSG = Column(String(1024))                                         # 留言信息
    PHONE = Column(String(96))                                         # 联系电话，不给前台看。只提供给管理员
    GRADE = Column(String(96))                                         # 年级
    MAJOR = Column(String(96))                                         # 专业
    SEEN_CNT = Column(Integer)                                         # 被查看的次数
    FORWARD_CNT = Column(Integer)                                      # 被转发的次数
    NICK_NAME = Column(String(96))                                     # 发布者的名字，可以是匿名
    GENDER = Column(String(32))                                        # 发布者的性别
    DATE_TIME = Column(DateTime, nullable=False)                       # 时间日期

    def __init__(self, user_id, object_id, object_name, object_class, object_status, img_url, msg, phone, grade,
                 major, seen_cnt, forward_cnt, nick_name, gender, date_time):
        self.OPEN_ID = user_id
        self.OBJECT_ID = object_id
        self.OBJECT_NAME = object_name
        self.OBJECT_CLASS = object_class
        self.OBJECT_STATUS = object_status
        self.IMG_URL = img_url
        self.MSG = msg
        self.PHONE = phone
        self.GRADE = grade
        self.MAJOR = major
        self.SEEN_CNT = seen_cnt
        self.FORWARD_CNT = forward_cnt
        self.NICK_NAME = nick_name
        self.GENDER = gender
        self.DATE_TIME = date_time


def parse_object(*args):
    """
    将查询到的结果转换为需要的结构，取出对象中的数据
    :param args:
    :return:
    """
    results = []
    for cond in args:
        result = {'OPEN_ID': cond.OPEN_ID,
                  'OBJECT_ID': cond.OBJECT_ID,
                  'OBJECT_NAME': cond.OBJECT_NAME,
                  'OBJECT_CLASS': cond.OBJECT_CLASS,
                  'OBJECT_STATUS': cond.OBJECT_STATUS,
                  'IMG_URL': cond.IMG_URL,
                  'MSG': cond.MSG,
                  'GRADE': cond.GRADE,
                  'MAJOR': cond.MAJOR,
                  'SEEN_CNT': cond.SEEN_CNT,
                  'FORWARD_CNT': cond.FORWARD_CNT,
                  'NICK_NAME': cond.NICK_NAME,
                  'GENDER': cond.GENDER,
                  'DATE_TIME': cond.DATE_TIME.strftime("%Y-%m-%d %H:%M:%S")}
        results.append(result)
    return results


def create_table():
    """
    新建一个found表
    :return:
    """
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL, encoding="utf-8")  # , echo=True
        # 执行创建表结构
        Base.metadata.create_all(engine)
        logging.info('OK: found.py--->create_table() 成功')
        return RESULT_OK
    except Exception as e:
        logging.critical('ERROR: found.py--->create_table() 失败: {}'.format(e))
        return RESULT_ERROR


def drop_table():
    """
    删除found表
    :return:
    """
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL, encoding="utf-8")  # , echo=True
        # 执行创建表结构
        Base.metadata.drop_all(engine)
        logging.info('OK: found.py--->drop_table() 成功')
        return RESULT_OK
    except Exception as e:
        logging.critical('ERROR: found.py--->drop_table() 失败: {}'.format(e))
        return RESULT_ERROR


def insert_data(**kwargs):
    """
    发布招领信息
    :param kwargs: {'user_id':user_id, 'object_name':object_name,‘object_class’: object_class,
    'object_status': object_status, 'img_url': img_url, 'msg': msg, 'phone': phone, 'grade':grade, 'major': major,
    'next_image': next_image, 'seen_cnt': seen_cnt, 'forward_cnt': forward_cnt, 'nick_name': nick_name}
    :return:
    """
    session = None
    try:
        session = get_session()
        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        img_url = '' if kwargs['img_url'] is None else kwargs['img_url']

        # 判断是不是连续传图，如果不是连续传图，则新增一条；
        # 如果是连续传图，则更新之前传的图像的 IMG_URL, 将当前的图像名与之前的图像名合成一个字符串，都逗号隔开
        if 'first' == kwargs['next_image'] or kwargs['next_image'] is None:
            # 传第一张图
            # 生成object_id
            object_id = gen_object_id(kwargs['user_id'], 'found')
            new_info = Found(user_id=kwargs['user_id'],
                             object_id=object_id,
                             object_name=kwargs['object_name'],
                             object_class=kwargs['object_class'],
                             object_status=config.INIT_FOUND_STUTAS,  # 初始化的状态
                             img_url=img_url,
                             msg=kwargs['msg'],
                             phone=kwargs['phone'],
                             grade=kwargs['grade'],
                             major=kwargs['major'],
                             nick_name=kwargs['nick_name'],
                             seen_cnt=0,                        # 初始化为0
                             forward_cnt=0,                     # 初始化为0
                             gender=kwargs['gender'],
                             date_time=_time)

            session.add(new_info)  # 添加
        else:
            # 连续传图模式，
            object_id = kwargs['next_image']
            _img_url = session.query(Found.IMG_URL).filter(Found.OBJECT_ID == object_id).first()
            new_img_url = _img_url.IMG_URL + ',' + img_url
            session.query(Found).filter(Found.OBJECT_ID == object_id).update({"IMG_URL": new_img_url})

        # 提交即保存到数据库
        session.commit()
        logging.info('OK : found.py--->insert_data() 成功')
        # 返回生成的object_id，解决多图上传问题
        return object_id
    except Exception as e:
        session.rollback()
        logging.critical('Error : found.py--->insert_data() 失败 : {}'.format(e))
        return RESULT_ERROR
    finally:
        session.close()


def del_data(**kwargs):
    """
    按照用户ID 与 OBJ_ID 删除发布的招领信息，两个条件同时满足才能执行删除操作
    :param kwargs: {'user_id': user_id, 'object_id' : object_id}
    :return:
    """
    session = None
    try:
        user_id, obj_id = kwargs['user_id'], kwargs['object_id']
        session = get_session()
        # 查询对应的图像的URL, 准备删除图像
        img = session.query(Found.IMG_URL).filter(Found.OPEN_ID == user_id, Found.OBJECT_ID == obj_id).first()
        # 指定数据删除
        session.query(Found).filter(and_(Found.OPEN_ID == user_id, Found.OBJECT_ID == obj_id)).delete()
        # 提交即保存到数据库
        session.commit()
        # 先完成数据库记录删除，再进行本地图像删除
        img = img.IMG_URL.split(',')
        for im in img:
            img_path = os.path.join(config.SERVER_IMAGE_DIR, im)
            # 判断文件是否存在，存在就删除
            if os.path.exists(img_path):
                os.remove(img_path)

        logging.info('OK : found.py--->del_data(), 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : found.py--->del_data()， 失败 ：{}'.format(e))
        return []
    finally:
        session.close()


def update_status(**kwargs):
    """
    更新招领物件的状态，只有发布信息的人才能操作
    :param kwargs: {'user_id': user_id, 'object_id': object_id, 'found_status': found_status}
    :return:
    """
    session = None
    try:
        user_id, obj_id, status = kwargs['user_id'], kwargs['object_id'], kwargs['object_status']
        session = get_session()
        session.query(Found).filter(and_(Found.OPEN_ID == user_id, Found.OBJECT_ID == obj_id)
                                          ).update({"OBJECT_STATUS": status})
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : found.py--->update_status() 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : found.py--->update_status() 失败 ：{}'.format(e))
        return RESULT_ERROR
    finally:
        session.close()


def update_seen_cnt(**kwargs):
    """
    更新被查看的次数，进行加1操作
    :param kwargs: {'object_id': object_id}
    :return:
    """
    session = None
    try:
        session = get_session()
        # 对SEEN_CNT做加1
        session.query(Found).filter(Found.OBJECT_ID == kwargs['object_id']).update(
                            {Found.SEEN_CNT: Found.SEEN_CNT + 1})
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : found.py--->update_seen_cnt(), 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : found.py--->update_seen_cnt() 失败 ：{}'.format(e))
        return []
    finally:
        session.close()


def update_forward_cnt(**kwargs):
    """
    更新被转发的次数，进行加1操作
    :param kwargs: {'object_id': object_id}
    :return:
    """
    session = None
    try:
        session = get_session()
        # 转发次数 +1
        session.query(Found).filter(Found.OBJECT_ID == kwargs['object_id']).update(
                            {Found.FORWARD_CNT: Found.FORWARD_CNT + 1})
        # 提交到数据库
        session.commit()
        logging.info('OK : found.py--->update_forward_cnt(), 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : found.py--->update_forward_cnt()  失败：{}'.format(e))
        return []
    finally:
        # 关闭session
        session.close()


def update_msg_cnt(**kwargs):
    """
    更新被转发的次数，进行加1操作
    :param kwargs: {'object_id': object_id, 'operator': 1},  condition['operator'] == 1, 增加一个, -1 减少一个
    :return:
    """
    session = None
    try:
        session = get_session()
        session.query(Found).filter(Found.OBJECT_ID == kwargs['object_id']).update(
                            {Found.MSG_CNT: Found.MSG_CNT + kwargs['operator']})
        # 提交到数据库
        session.commit()
        logging.info('OK : found.py--->update_msg_cnt(), 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()  # 执行失败，回滚数据
        logging.critical('Error : found.py--->update_msg_cnt() 失败：{}'.format(e))
        return []
    finally:
        session.close()


def query_by_seen():
    """
    查询被查看次数的降序
    :return:
    """
    session = None
    try:
        session = get_session()
        result = session.query(Found).order_by(Found.SEEN_CNT.desc(), Found.DATE_TIME.desc()
                                               ).limit(config.LIMIT_MAX).all()
        session.commit()
        results = parse_object(*result)
        logging.info('OK : found.py--->query_by_obj_seen() 成功 ')
        return results
    except Exception as e:
        logging.critical('Error : found.py--->query_by_obj_seen() 失败 : {}'.format(e))
        return []
    finally:
        session.close()


def query_by_forward():
    """
    查询被转发次数的降序
    :return:
    """
    session = None
    try:
        session = get_session()
        result = session.query(Found).order_by(
            Found.FORWARD_CNT.desc(), Found.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*result)
        logging.info('OK : found.py--->query_by_obj_seen(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : found.py--->query_by_obj_seen() 失败 : {}'.format(e))
        return []
    finally:
        session.close()


def query_by_name(**kwargs):
    """
    根据招领物件的名称查询
    :param kwargs: {'object_name': object_name}
    :return:
    """
    session = None
    try:
        session = get_session()
        # 用名称进行模糊查询
        object_name = '%' + kwargs['object_name'] + '%'
        result = session.query(Found).filter(Found.OBJECT_NAME.like(object_name)).order_by(
                            Found.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*result)
        logging.info('OK : found.py--->query_by_name(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : found.py--->query_by_name() 失败 : {}'.format(e))
        return []
    finally:
        # 关闭session
        session.close()


def query_by_class(**kwargs):
    """
    根据招领物件的类别查询
    :param kwargs: {'object_class': object_class}
    :return:
    """
    session = None
    try:
        session = get_session()
        object_class = kwargs['object_class']
        result = session.query(Found).filter(Found.OBJECT_CLASS.like(object_class)).order_by(
                            Found.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*result)
        logging.info('OK : found.py--->query_by_class(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : found.py--->query_by_class() 失败 : {}'.format(e))
        return []
    finally:
        # 关闭session
        session.close()


def query_by_found_id(**kwargs):
    """
    根据招领物件的id查询
    :param kwargs: {'object_id': object_id}
    :return:
    """
    session = None
    try:
        session = get_session()
        result = session.query(Found).filter(Found.OBJECT_ID == kwargs['object_id']).order_by(
                            Found.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*result)
        logging.info('OK : found.py--->query_by_name(), 成功')

        return results
    except Exception as e:
        logging.critical('Error : found.py--->query_by_name() 失败 : {}'.format(e))
        return []
    finally:
        # 关闭session
        session.close()


def query_by_user_id(**kwargs):
    """
    根据发布招领物件人的id查询
    :param kwargs: {'user_id': user_id}
    :return:
    """
    session = None
    try:
        session = get_session()
        result = session.query(Found).filter(Found.OPEN_ID == kwargs['user_id']).order_by(
            Found.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*result)
        logging.info('OK : found.py--->query_by_name(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : found.py--->query_by_name() 失败 : {}'.format(e))
        return []
    finally:
        session.close()


def query_by_date_before(**kwargs):
    """
    根据发布的时间查询，之前的记录： 2020-06-03之前，即2020-06-03, 2020-06-02, ......
    :param kwargs: {'date': date}
    :return:
    """
    session = None
    try:
        session = get_session()
        date = kwargs['date'].strip() + config.END_DAY_TIME
        result = session.query(Found).filter(Found.DATE_TIME <= date).order_by(
                 Found.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*result)
        logging.info('OK : found.py--->query_by_date_before(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : found.py--->query_by_date_before() 失败 : {}'.format(e))
        return []
    finally:
        session.close()


def query_by_date_after(**kwargs):
    """
    根据发布的时间查询，之后的记录： 2020-06-03之后，即2020-06-03, 2020-06-04, ......
    :param kwargs: {'date': date}
    :return:
    """
    session = None
    try:
        session = get_session()
        date = kwargs['date'].strip() + config.BEGIN_DAY_TIME
        result = session.query(Found).filter(
                            Found.DATE_TIME >= date).order_by(Found.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        session.commit()
        results = parse_object(*result)
        logging.info('OK : found.py--->query_by_date_after(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : found.py--->query_by_date_after() 失败 : {}'.format(e))
        return []
    finally:
        session.close()


def query_by_date_between(**kwargs):
    """
    根据发布的时间查询，之间的记录
    :param kwargs: {'date': date}， data='2020-06-01, 2020-06-03'
    :return:
    """
    session = None
    try:
        data_start, data_end = kwargs['date'].split(',')
        date_start = data_start.strip() + config.BEGIN_DAY_TIME
        date_end = data_end.strip() + config.END_DAY_TIME

        session = get_session()
        result = session.query(Found).filter(and_(Found.DATE_TIME >= date_start, Found.DATE_TIME <= date_end)).order_by(
                            Found.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        session.commit()
        results = parse_object(*result)
        logging.info('OK : found.py--->query_by_date_between(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : found.py--->query_by_date_between() 失败 : {}'.format(e))
        return []
    finally:
        session.close()


if __name__ == '__main__':
    # drop_table()
    create_table()
    # ret = insert_data(**condition)
    # ret = del_data(**{'user_id': 'o7C2I5K-2wGlMbKaMNk0IsXg2U6g',
    #                 'object_id': 'found_751896_o7C2I5K-2wGlMbKaMNk0IsXg2U6g'})
    # ret = update_seen_cnt(**{'object_id': 'found_719564_0'})
    # ret = update_forward_cnt(**{'object_id': 'found_719564_0'})

    # res = query_by_forward()
    # res = query_by_seen()
    # res = query_by_name(**{'object_name': '英语课本'})
    # res = query_by_class(**{'object_class': '书籍'})
    # res = query_by_user_id(**{'user_id': '0'})
    # res = query_by_found_id(**{'object_id': 'found_719564_0'})
    # res = query_by_date_before(**{'date': '2020-06-19'})
    # res = query_by_date_after(**{'date': '2020-06-08'})
    # res = query_by_date_between(**{'date': '2020-06-01, 2020-06-17'})

