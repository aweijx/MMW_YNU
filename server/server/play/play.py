# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述： 发布约打球信息，以及查询和状态更新，等信息
# 主要函数：
#         1.  create_table
#         2.  drop_table
#         3.  insert_data
#         4.  del_data
#         5.  update_status
#         6.  update_seen_cnt
#         7.  update_forward_cnt
#         8.  query_by_seen
#         9.  query_by_forward
#         10. query_by_name
#         11. query_by_class
#         12. query_by_found_id
#         13. query_by_user_id
#         14. query_by_date_before
#         15. query_by_date_after
#         16. query_by_date_between
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
from sqlalchemy import Column, Integer, String,  DateTime, and_
from utils import RESULT_ERROR, RESULT_OK, RESULT_FAILED, get_session, gen_object_id

# 生成ORM基类
Base = declarative_base()


class Play(Base):
    """
    新建约打球信息表
    """
    __tablename__ = "play_info"                                        # 表名
    ID = Column(Integer, primary_key=True, autoincrement=True)         # 自增编号
    OPEN_ID = Column(String(96), nullable=False)                       # 微信用户的openid
    OBJECT_ID = Column(String(96), nullable=False, unique=True)        # 约球信息的ID
    SUBJECT = Column(String(96), nullable=False)                       # 具体哪一种球，篮球/羽毛球/乒乓球 ...
    IMG_URL = Column(String(2048))                                     # image url
    MSG = Column(String(1024))                                         # 详情信息
    PHONE = Column(String(96))                                         # 联系电话，不给前台看。只提供给管理员
    GRADE = Column(String(96))                                         # 年级
    MAJOR = Column(String(96))                                         # 专业
    SEEN_CNT = Column(Integer)                                         # 被查看的次数
    FORWARD_CNT = Column(Integer)                                      # 被转发的次数
    NICK_NAME = Column(String(96))                                     # 发布者的名字，可以是匿名
    GENDER = Column(String(32))                                        # 发布者的性别
    DATE_TIME = Column(DateTime, nullable=False)                       # 时间日期

    def __init__(self, user_id, object_id, subject, img_url, msg, phone, grade, major, seen_cnt, forward_cnt,
                 nick_name, gender, date_time):
        self.OPEN_ID = user_id
        self.OBJECT_ID = object_id
        self.SUBJECT = subject
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
    将查询到的结果转换为需要的结构
    :param args:
    :return:
    """
    results = []
    for cond in args:
        result = {'OPEN_ID': cond.OPEN_ID,
                  'OBJECT_ID': cond.OBJECT_ID,
                  'SUBJECT': cond.SUBJECT,
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
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL, encoding="utf-8")  # , echo=True
        # 执行创建表结构
        Base.metadata.create_all(engine)
        logging.info('OK: play.py--->create_table, 成功')
        return RESULT_OK
    except Exception as e:
        logging.critical('ERROR: play.py--->create_table 失败 {}'.format(e))
        return RESULT_FAILED


def drop_table():
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL, encoding="utf-8")  # , echo=True
        # 执行创建表结构
        Base.metadata.drop_all(engine)
        logging.info('OK: play.py--->drop_table, 成功')
        return RESULT_OK
    except Exception as e:
        logging.critical('ERROR: play.py--->drop_table 失败 {}'.format(e))
        return RESULT_FAILED


def insert_data(**kwargs):
    """
    发布学习信息
    :param kwargs: {'user_id':user_id, 'subject':subject, 'img_url': img_url, 'msg': msg, 'phone': phone,
    'grade': grade, 'major':major, 'nick_name':nick_name, 'gender': gender}
    :return:
    """
    session = None
    try:
        session = get_session()
        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        _img_url = '' if kwargs['img_url'] is None else kwargs['img_url']

        # 判断是不是连续传图，如果不是连续传图，则新增一条；
        # 如果是连续传图，则更新之前传的图像的 IMG_URL, 将当前的图像名与之前的图像名合成一个字符串，都逗号隔开
        if 'first' == kwargs['next_image']:
            # 传第一张图
            # 生成object_id
            object_id = gen_object_id(user_id=kwargs['user_id'], object_class='play')
            new_info = Play(user_id=kwargs['user_id'],
                            object_id=object_id,
                            subject=kwargs['subject'],
                            img_url=_img_url,
                            phone=kwargs['phone'],
                            grade=kwargs['grade'],
                            msg=kwargs['msg'],
                            major=kwargs['major'],
                            nick_name=kwargs['nick_name'],
                            seen_cnt=0,                           # 初始化为0
                            forward_cnt=0,                        # 初始化为0
                            gender=kwargs['gender'],
                            date_time=_time)

            session.add(new_info)
        else:
            # 连续传图模式，
            object_id = kwargs['next_image']
            _img_url = session.query(Play.IMG_URL).filter(Play.OBJECT_ID == object_id).first()
            new_img_url = _img_url.IMG_URL + ',' + _img_url
            session.query(Play).filter(Play.OBJECT_ID == object_id).update({"IMG_URL": new_img_url})

        session.commit()
        logging.info('OK : study_info.py--->insert_data(), 成功')
        return object_id
    except Exception as e:
        # 出错时，回滚一下清数据
        session.rollback()
        logging.critical('Error : study_info.py--->insert_data() 失败: {}'.format(e))
        return RESULT_ERROR
    finally:
        session.close()


def del_data(**kwargs):
    """
    按照用户ID 与 OBJECT_ID 删除发布信息，两个条件同时满足才能执行删除操作
    :param kwargs: {'user_id': user_id, 'object_id' : object_id}
    :return:
    """
    session = None
    try:
        user_id, object_id = kwargs['user_id'], kwargs['object_id']
        session = get_session()
        # 查询对应的图像的URL, 准备删除图像
        img = session.query(Play.IMG_URL).filter(Play.OPEN_ID == user_id, Play.OBJECT_ID == object_id).first()
        # 指定数据删除
        session.query(Play).filter(and_(Play.OPEN_ID == user_id, Play.OBJECT_ID == object_id)).delete()
        # 提交即保存到数据库
        session.commit()
        # 先完成数据库记录删除，再进行本地图像删除
        img = img.IMG_URL.split(',')
        for im in img:
            img_path = os.path.join(config.SERVER_IMAGE_DIR, im)
            # 判断文件是否存在，存在就删除
            if os.path.exists(img_path):
                os.remove(img_path)

        logging.info('OK : play.py--->del_data(), 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : play.py--->del_data() 失败 : {}'.format(e))
        return []
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
        session.query(Play).filter(Play.OBJECT_ID == kwargs['object_id']).update(
            {Play.SEEN_CNT: Play.SEEN_CNT + 1})
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : play.py--->update_see_cnt() 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : play.py--->update_see_cnt() 失败：{}'.format(e))
        return []
    finally:
        # 关闭session
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
        # 对 FORWARD_CNT 做加1
        session.query(Play).filter(Play.OBJECT_ID == kwargs['object_id']).update(
            {Play.FORWARD_CNT: Play.FORWARD_CNT + 1})
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : play.py--->update_forward_cnt() 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : play.py--->update_forward_cnt() 失败：{}'.format(e))
        return []
    finally:
        session.close()


def update_msg_cnt(**kwargs):
    """
    更新评论的次数，进行加1操作，减1操作
    :param kwargs: {'object_id': object_id, 'operator': 1},  condition['operator'] == 1, 增加一个, -1 减少一个
    :return:
    """
    session = None
    try:
        session = get_session()
        session.query(Play).filter(Play.OBJECT_ID == kwargs['object_id']).update(
                            {Play.MSG_CNT: Play.MSG_CNT + kwargs['operator']})
        # 提交到数据库
        session.commit()
        logging.info('OK : play.py--->update_msg_cnt() 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : play.py--->update_msg_cnt() 失败：{}'.format(e))
        return []
    finally:
        # 关闭session
        session.close()


def query_by_seen():
    """
    查询被查看次数的降序
    :return:
    """
    session = None
    try:
        session = get_session()
        ret = session.query(Play).order_by(Play.SEEN_CNT.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : play.py--->query_by_seen() 成功')
        return results
    except Exception as e:
        logging.critical('Error : play.py--->query_by_seen() 失败: {}'.format(e))
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
        ret = session.query(Play).order_by(Play.FORWARD_CNT.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : play.py--->query_by_forward(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : play.py--->query_by_forward() 失败: {}'.format(e))
        return []
    finally:
        session.close()


def query_by_subject(**kwargs):
    """
    根据学科名称查询
    :param kwargs: {'subject': subject}
    :return:
    """
    session = None
    try:
        subject = '%' + kwargs['subject'] + '%'
        session = get_session()
        ret = session.query(Play).filter(Play.SUBJECT.like(subject)).order_by(
                            Play.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : play.py--->query_by_subject(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : play.py--->query_by_subject() 失败 : {}'.format(e))
        return []
    finally:
        session.close()


def query_by_study_id(**kwargs):
    """
    根据学习信息的id查询
    :param kwargs: {'object_id': object_id}
    :return:
    """
    session = None
    try:
        object_id = kwargs['object_id']
        session = get_session()
        ret = session.query(Play).filter(Play.OBJECT_ID == object_id).order_by(
                            Play.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()

        # ret = session.query(message.Message).filter(Play).limit(config.LIMIT_MAX).all()

        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : play.py--->query_by_name(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : play.py--->query_by_name() 失败: {}'.format(e))
        return []
    finally:
        session.close()


def query_by_user_id(**kwargs):
    """
    根据发布招领物件人的id查询
    :param kwargs: {'user_id': user_id}
    :return:
    """
    session = None
    try:
        user_id = kwargs['user_id']
        session = get_session()
        ret = session.query(Play).filter(Play.OPEN_ID == user_id).order_by(
                            Play.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : play.py--->query_by_name(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : play.py--->query_by_name() 失败 : {}'.format(e))
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
        date = kwargs['date'].strip() + config.END_DAY_TIME
        session = get_session()
        ret = session.query(Play).filter(Play.DATE_TIME <= date).order_by(
                            Play.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : play.py--->query_by_date_before(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : play.py--->query_by_date_before() 失败 : {}'.format(e))
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
        date = kwargs['date'].strip() + config.BEGIN_DAY_TIME
        session = get_session()
        ret = session.query(Play).filter(Play.DATE_TIME >= date).order_by(
                            Play.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : play.py--->query_by_date_after(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : play.py--->query_by_date_after() 失败: {}'.format(e))
        return []
    finally:
        # 关闭session
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
        ret = session.query(Play).filter(Play.DATE_TIME >= date_start, Play.DATE_TIME <= date_end
                                         ).order_by(Play.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : play.py--->query_by_date_between(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : play.py--->query_by_date_between() 失败: {}'.format(e))
        return []
    finally:
        session.close()


if __name__ == '__main__':
    # drop_table()
    create_table()
    # res = insert_data(**condition)
    # ret = del_data(**{'user_id': '0', 'object_id': 'play_700442_0'})
    # update_seen_cnt(**{'object_id': 'play_648313_0'})
    # update_forward_cnt(**{'object_id': 'play_648313_0'})
    # update_msg_cnt(**{'object_id': 'play_648313_0', 'operator': 1})
    # res = query_by_forward()
    # res = query_by_seen()
    # res = query_by_user_id(**{'user_id': '0'})
    # res = query_by_study_id(**{'object_id': 'play_774998_7'})
    # res = query_by_subject(**{'subject': '棒'})
    # res = query_by_date_before(**{'date': '2020-06-15'})
    # res = query_by_date_after(**{'date': '2020-06-07'})
    # res = query_by_date_between(**{'date': '2020-06-05, 2020-06-18'})

