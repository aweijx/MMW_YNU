# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述：菜鸟编程信息表文件，发布/更新/查询/删除
# 主要函数：     1.  create_table()
#              2.  drop_table()
#              3.  insert_data( )
#              4.  del_data()
#              5.  update_seen_cnt()
#              6.  update_forward_cnt()
#              7.  query_by_forward()
#              8.  query_by_seen()
#              9.  query_by_user_id()
#              10. query_by_study_id()
#              11. query_by_subject()
#              12. query_by_date_before()
#              13. query_by_date_after()
#              14. query_by_date_between()
#
# 作者: 方成
# 单位： 云南大学信息学院
# 生成日期：2020-11-01
# ----------------------------------------------------------------------------- #
import config
import logging
import time
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from utils import RESULT_ERROR, RESULT_OK, RESULT_FAILED, get_session, gen_object_id

# 生成ORM基类
Base = declarative_base()


class Code(Base):
    """
    菜鸟编程信息表
    """
    __tablename__ = "code_info"                                        # 表名
    ID = Column(Integer, primary_key=True, autoincrement=True)         # 自增编号
    OPEN_ID = Column(String(64), nullable=False)                       # 微信用户的openid
    OBJECT_ID = Column(String(64), nullable=False, unique=True)        # ID
    SUBJECT = Column(String(128))                                      # 科目
    IMG_URL = Column(String(2048))                                     # 图像
    MSG = Column(String(1024))                                         # 留言信息
    PHONE = Column(String(64))                                         # 联系电话
    GRADE = Column(String(128))                                        # 年级
    MAJOR = Column(String(128))                                        # 专业
    SEEN_CNT = Column(Integer)                                         # 被查看的次数
    FORWARD_CNT = Column(Integer)                                      # 被转发的次数
    NICK_NAME = Column(String(128))                                    # 发布者的名字
    GENDER = Column(String(32))                                        # 发布者的性别
    DATE_TIME = Column(DateTime, nullable=False)                       # 时间日期

    def __init__(self, user_id, subject, object_id, img_url, msg, phone, grade, major,
                 seen_cnt, forward_cnt, nick_name, gender, date_time):
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
    result = []
    for cond in args:
        r = {'OPEN_ID': cond.OPEN_ID,
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
        result.append(r)

    return result


def create_table():
    try:
        # 连接数据库
        engine = create_engine(config.DB_URL, encoding=config.DB_ENCODE)
        # 执行创建表结构
        Base.metadata.create_all(engine)
        logging.info('OK: contest.py--->create_table(), 成功！')
        return RESULT_OK
    except Exception as e:
        logging.critical('ERROR: code.py--->create_table() 失败！ {0}'.format(e))
        return RESULT_FAILED


def drop_table():
    try:
        # 连接数据库
        engine = create_engine(config.DB_URL, encoding=config.DB_ENCODE)
        # 执行创建表结构
        Base.metadata.drop_all(engine)
        logging.info('OK: code.py--->drop_table(), 成功！')
        return RESULT_OK
    except Exception as e:
        logging.critical('ERROR: code.py--->drop_table() 失败！ {0}'.format(e))
        return RESULT_FAILED


def insert_data(**kwargs):
    """
    添加一条新的信息
    :param kwargs: {}
    :return:
    """
    session = None
    try:
        session = get_session()
        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        img_url = '' if kwargs['img_url'] is None else kwargs['img_url']

        if 'first' == kwargs['next_image']:
            object_id = gen_object_id(user_id=kwargs['user_id'], object_class='code')
            new_info = Code(user_id=kwargs['user_id'],
                            object_id=object_id,
                            subject=kwargs['subject'],
                            img_url=img_url,
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
            _img_url = session.query(Code.IMG_URL).filter(Code.OBJECT_ID == object_id).first()
            new_img_url = _img_url.IMG_URL + ',' + img_url
            session.query(Code).filter(Code.OBJECT_ID == object_id).update({"IMG_URL": new_img_url})

        # 提交即保存到数据库
        session.commit()
        logging.info('OK : code.py--->insert_data(), 成功添加一条丢失信息')
        # 返回生成的object_id，解决多图上传问题
        return object_id
    except Exception as e:
        # 出错时，回滚一下
        session.rollback()
        logging.critical('Error : code.py--->insert_data() : {0}'.format(e))
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
        img = session.query(Code.IMG_URL).filter(Code.OPEN_ID == user_id, Code.OBJECT_ID == object_id).first()
        # 指定数据删除
        session.query(Code).filter(Code.OPEN_ID == user_id, Code.OBJECT_ID == object_id).delete()
        # 提交即保存到数据库
        session.commit()
        # 先完成数据库记录删除，再进行本地图像删除
        img = img.IMG_URL.split(',')
        for im in img:
            img_path = os.path.join(config.SERVER_IMAGE_DIR, im)
            # 判断文件是否存在，存在就删除
            if os.path.exists(img_path):
                os.remove(img_path)

        logging.info('OK : code.py--->del_data(), 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : code.py--->del_data() 失败 : {}'.format(e))
        return []
    finally:
        # 关闭session
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
        session.query(Code).filter(Code.OBJECT_ID == kwargs['object_id']).update(
            {Code.SEEN_CNT: Code.SEEN_CNT + 1})
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : code.py--->update_see_cnt()')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : code.py--->update_see_cnt()--->{}'.format(e))
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
        session.query(Code).filter(Code.OBJECT_ID == kwargs['object_id']).update(
            {Code.FORWARD_CNT: Code.FORWARD_CNT + 1})
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : code.py--->update_forward_cnt()')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : code.py--->update_forward_cnt()--->{}'.format(e))
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
        session.query(Code).filter(Code.OBJECT_ID == kwargs['object_id']).update(
                            {Code.MSG_CNT: Code.MSG_CNT + kwargs['operator']})
        # 提交到数据库
        session.commit()
        logging.info('OK : code.py--->update_msg_cnt(), 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : code.py--->update_msg_cnt()---> 失败：{}'.format(e))
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
        ret = session.query(Code).order_by(Code.SEEN_CNT.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : code.py--->query_by_seen(), 成功查询到 {} 条丢失信息.'.format(len(results)))
        return results
    except Exception as e:
        logging.critical('Error : code.py--->query_by_seen() : {0}'.format(e))
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
        ret = session.query(Code).order_by(Code.FORWARD_CNT.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : code.py--->query_by_forward(), 成功查询到 {} 条信息.'.format(len(results)))
        return results
    except Exception as e:
        logging.critical('Error : code.py--->query_by_forward() : {0}'.format(e))
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
        ret = session.query(Code).filter(Code.SUBJECT.like(subject)).order_by(
                            Code.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : code.py--->query_by_subject(), 成功查询到 {} 条信息.'.format(len(results)))
        return results
    except Exception as e:
        logging.critical('Error : code.py--->query_by_subject() 失败 : {0}'.format(e))
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
        ret = session.query(Code).filter(Code.OBJECT_ID == object_id).order_by(
                            Code.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # ret = session.query(message.Message).filter(Play).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : code.py--->query_by_name(), 成功查询到 {} 条丢失信息.'.format(len(results)))
        return results
    except Exception as e:
        logging.critical('Error : code.py--->query_by_name() : {0}'.format(e))
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
        user_id = kwargs['user_id']
        session = get_session()
        ret = session.query(Code).filter(Code.OPEN_ID == user_id).order_by(
                            Code.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : code.py--->query_by_name(), 成功查询到 {} 条丢失信息.'.format(len(results)))
        return results
    except Exception as e:
        logging.critical('Error : code.py--->query_by_name() 失败 : {0}'.format(e))
        return []
    finally:
        # 关闭session
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
        ret = session.query(Code).filter(Code.DATE_TIME <= date).order_by(
                            Code.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : code.py--->query_by_date_before(), 成功查询到 {} 条信息.'.format(len(results)))
        return results
    except Exception as e:
        logging.critical('Error : code.py--->query_by_date_before() 失败 : {0}'.format(e))
        return []
    finally:
        # 关闭session
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
        ret = session.query(Code).filter(Code.DATE_TIME >= date).order_by(
                            Code.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : code.py--->query_by_date_after(), 成功查询到 {} 条丢失信息.'.format(len(results)))
        return results
    except Exception as e:
        logging.critical('Error : code.py--->query_by_date_after() : {0}'.format(e))
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
        ret = session.query(Code).filter(Code.DATE_TIME >= date_start, Code.DATE_TIME <= date_end
                                         ).order_by(Code.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(*ret)
        logging.info('OK : code.py--->query_by_date_between(), 成功查询到 {} 条丢失信息.'.format(len(results)))
        return results
    except Exception as e:
        logging.critical('Error : code.py--->query_by_date_between() : {0}'.format(e))
        return []
    finally:
        # 关闭session
        session.close()


if __name__ == '__main__':
    # drop_table()
    create_table()
