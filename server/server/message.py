# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述： 留言信息
# 主要模块：
#          1. drop_table()
#          2. create_table()
#          3. insert_data()
#          4. del_data()
#          5. query_msg_by_obj()
#          6. query_msg_by_user()
#          7. query_msg()
#
# 作者: 方成
# 单位： 云南大学信息学院
# 生成日期：2020-10-26
# ----------------------------------------------------------------------------- #
import config
import logging
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, and_, func, or_
from utils import RESULT_ERROR, RESULT_OK, RESULT_FAILED, get_session, gen_object_id
from found import found
from play import play
from second_hand import second_hand
from study import study

# 生成ORM基类
Base = declarative_base()


class Message(Base):
    """
    留言信息表
    """
    __tablename__ = "message_info"                                     # 表名
    ID = Column(Integer, primary_key=True, autoincrement=True)         # 自增编号
    OPEN_ID = Column(String(96), nullable=False)                       # 微信用户的openid
    OBJECT_ID = Column(String(128), nullable=False)                    # 丢失物的ID
    MSG_ID = Column(String(128))                                       # 消息ID
    NICK_NAME = Column(String(96))                                     # 昵称
    GENDER = Column(String(64))                                        # 性别
    MSG = Column(String(512))                                          # 留言信息
    TARGET_ID = Column(String(128), nullable=False)                    # 给谁留言
    GROUP_ID = Column(Integer, nullable=False)                         # 留言分组编号
    DATE_TIME = Column(DateTime, nullable=False)                       # 时间日期

    def __init__(self, user_id, object_id, msg_id, nick_name, gender, target_id, group_id, msg, date_time):
        self.OPEN_ID = user_id
        self.OBJECT_ID = object_id
        self.MSG_ID = msg_id
        self.GENDER = gender
        self.NICK_NAME = nick_name
        self.TARGET_ID = target_id
        self.MSG = msg
        self.GROUP_ID = group_id
        self.DATE_TIME = date_time


def parse_object(condition=None):
    """
    将查询到的结果转换为需要的结构
    :param condition:
    :return:
    """
    result = []
    for cond in condition:
        r = {'OPEN_ID': cond.OPEN_ID,
             'OBJECT_ID': cond.OBJECT_ID,
             'MSG': cond.MSG,
             'NICK_NAME': cond.NICK_NAME,
             'GENDER': cond.GENDER,
             'MSG_ID': cond.MSG_ID,
             'TARGET_ID': cond.TARGET_ID,
             'GROUP_ID': cond.GROUP_ID,
             'DATE_TIME': cond.DATE_TIME.strftime("%Y-%m-%d %H:%M:%S")}
        result.append(r)
    return result


def parse_group(condition=None):
    """
    把结果分组包装，按照group_id
    :param condition:
    :return:
    """
    res, results = [], []
    group_id = 0
    for index, cond in enumerate(condition):

        if group_id == cond['GROUP_ID']:
            res.append(cond)
        else:
            results.append(res)
            group_id = cond['GROUP_ID']
            res = []
            res.append(cond)

    results.append(res)  # 最后
    return results


def create_table():
    try:
        # 连接数据库
        connect = create_engine(config.DB_URL, encoding="utf-8")
        # 执行创建表结构
        Base.metadata.create_all(connect)
        logging.info('create table: msg_info 成功！')
        return RESULT_OK
    except Exception as e:
        logging.critical('create table: msg_info 失败！ {0}'.format(e))
        return RESULT_FAILED


def drop_table():
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL, encoding=config.DB_ENCODE)
        # 执行创建表结构
        Base.metadata.drop_all(engine)
        logging.info('OK: msg_table.py--->drop_table() 成功！')
        return RESULT_OK
    except Exception as e:
        logging.critical('ERROR: msg_table.py--->drop_table() 失败！ {0}'.format(e))
        return RESULT_FAILED


def insert_data(**kwargs):
    """
    新增发布丢失信息
    :param kwargs: {'user_id':user_id, 'object_id':object_id, 'nick_name':nick_name,
                 'gender': gender, 'msg': msg, 'target_id':target_id, 'group_id':group_id, 'date_time': date_time}
    :return:
    """
    session = None
    try:
        session = get_session()
        nick_name = '' if kwargs['nick_name'] is None else kwargs['nick_name']
        gender = '' if kwargs['gender'] is None else kwargs['gender']
        _msg = '' if kwargs['msg'] is None else kwargs['msg']
        if isinstance(kwargs['group_id'], str):
            # 转换为int型
            kwargs['group_id'] = int(kwargs['group_id'])

        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msg_id = gen_object_id(kwargs['user_id'], 'msg')
        new_msg = Message(user_id=kwargs['user_id'],
                          object_id=kwargs['object_id'],
                          msg_id=msg_id,
                          nick_name=nick_name,
                          gender=gender,
                          target_id=kwargs['target_id'],
                          group_id=kwargs['group_id'],
                          msg=_msg,
                          date_time=_time)

        session.add(new_msg)
        # 提交到数据库
        session.commit()
        logging.info('OK : message.py--->insert_data(), 成功')
        # 对应的留言数加1
        # result = update_msg_cnt({'object_id': condition['object_id'], 'operator': 1})
        return RESULT_OK
    except Exception as e:
        # 出错时，回滚一下清楚数据
        session.rollback()
        logging.critical('Error : message.py--->insert_data() 失败: {0}'.format(e))
        return RESULT_ERROR
    finally:
        session.close()


def del_data(**kwargs):
    """
    按照用户ID 与 OBJ_ID 删除发布的信息，两个条件同时满足才能执行删除操作
    :param kwargs: {'user_id': user_id, 'object_id' : object_id}
    :return:
    """
    session = None
    try:
        user_id, object_id = kwargs['user_id'], kwargs['object_id']
        session = get_session()
        session.query(Message).filter(and_(Message.OPEN_ID == user_id, Message.OBJECT_ID == object_id)).delete()
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : message.py--->del_data() 成功 ')
        # 对应的found, play, study, second-hand 的 MSG_CNT 减一
        # result = update_msg_cnt({'object_id': condition['object_id'], 'operator': -1})
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : message.py--->del_data(), 执行操作失败： {}'.format(e))
        return RESULT_ERROR
    finally:
        # 关闭session
        session.close()


def del_by_message_id(**kwargs):
    """
    根据消息的ID删除一条消息，
    如果删除的是分组的第一条留言，则将整个分组都删除，否则只删除指定的一条留言
    :param kwargs: {'message_id': message_id, 'object_id': object_id}
    :return:
    """
    message_id = kwargs['message_id']
    object_id = kwargs['object_id']

    session = None
    try:
        session = get_session()
        # 1.查询的分组编号
        group_id = session.query(Message.GROUP_ID).filter(and_(Message.MSG_ID == message_id, Message.OBJECT_ID == object_id)
                                 ).limit(config.LIMIT_MAX).scalar()

        # 2.查询分组编号对应的时间排序的第一条记录
        group_first = session.query(Message).filter(Message.GROUP_ID == group_id, Message.OBJECT_ID == object_id
                                                    ).order_by(Message.DATE_TIME.asc()).limit(config.LIMIT_MAX).first()

        _message_id, _object_id = group_first.MSG_ID, group_first.OBJECT_ID
        if _message_id == message_id and _object_id == object_id:
            # 如果要删除的是第一条留言，则整个留言组全部删掉
            session.query(Message).filter(and_(Message.OBJECT_ID == object_id, Message.GROUP_ID == group_id)).delete()
        else:
            # 否则，只删除指定的一条留言
            session.query(Message).filter(Message.MSG_ID == message_id, Message.OBJECT_ID == object_id).delete()

        # 提交即保存到数据库
        session.commit()
        logging.info('OK : message.py--->del_by_message_id() 执行删除操作成功 ')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : message.py--->del_by_message_id(), 执行操作失败： {}'.format(e))
        return RESULT_ERROR
    finally:
        session.close()


def query_msg_by_obj(**kwargs):
    """
   根据obj_id查询所有相关的留言，用于点开信息详情的页面
   :param kwargs: {'object_id': object_id}
    :return: 返回所有的留言信息
    """
    session = None
    try:
        object_id = kwargs['object_id']
        session = get_session()
        result = session.query(Message).filter(Message.OBJECT_ID == object_id
                              ).order_by(Message.GROUP_ID.asc(), Message.DATE_TIME.asc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(result)
        results = parse_group(results)
        logging.info('OK : message.py--->query_msg_by_obj() 成功 ')
        return results
    except Exception as e:
        session.rollback()
        logging.critical('Error : message.py--->query_msg_by_obj()  失败 : {}'.format(e))
        return []
    finally:
        session.close()


def query_msg_by_user(**kwargs):
    """
   根据user_id查询所有相关的留言，用于点开信息详情的页面
   :param kwargs: {'user_id': user_id}
    :return: 返回所有的留言信息
    """
    session = None
    try:
        session = get_session()
        result = session.query(Message).filter(Message.OPEN_ID == kwargs['user_id']
                                               ).order_by(Message.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(result)
        logging.info('OK : message.py--->query_msg_by_user()  成功 ')
        return results
    except Exception as e:
        session.rollback()
        logging.critical('Error : message.py--->query_msg_by_user()  失败 : {}'.format(e))
        return []
    finally:
        session.close()


def query_msg_to_user(**kwargs):
    """
   查询别人给自己的留言
   :param kwargs: {'user_id': user_id}
    :return: 返回所有的留言信息
    """
    session = None
    try:
        session = get_session()
        result = session.query(Message).filter(Message.TARGET_ID == kwargs['user_id']
                                               ).order_by(Message.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(result)
        logging.info('OK : message.py--->query_msg_to_user()  成功 ')
        return results
    except Exception as e:
        session.rollback()
        logging.critical('Error : message.py--->query_msg_to_user()  失败 : {}'.format(e))
        return []
    finally:
        session.close()


def query_msg_cnt_by_obj(*args):
    """
    通过object_id查询留言数量，这个函数只是用来修改 query_xxxx 中的 MSG_CNT字段的值
    :param kwargs: {'object_id': object_id}
    :return:
    """
    session = None
    try:
        session = get_session()
        for cond in args:
            cond['MSG_CNT'] = session.query(func.count('*')).filter(Message.OBJECT_ID == cond['OBJECT_ID']).scalar()

        session.commit()
        return args
    except Exception:
        session.rollback()
        return args
    finally:
        session.close()


def query_msg(**kwargs):
    """
   根据user_id和obj_id查询指定的留言
   :param kwargs: {‘object_id’: object_id, 'user_id': user_id}
    :return: 返回所有的留言信息
    """
    session = None
    try:
        user_id, obj_id = kwargs['user_id'], kwargs['object_id']

        session = get_session()
        result = session.query(Message).filter(and_(Message.OPEN_ID == user_id, Message.OBJECT_ID == obj_id)).order_by(
                            Message.DATE_TIME.desc()).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = parse_object(result)
        logging.info('OK : message.py--->query_msg() 成功')
        return results
    except Exception as e:
        session.rollback()
        logging.critical('Error : message.py--->query_msg()  失败 : {}'.format(e))
        return []
    finally:
        session.close()


if __name__ == '__main__':
    # drop_table()
    create_table()
    # del_by_message_id(object_id='study_344139_0', message_id='msg_71296_2')

