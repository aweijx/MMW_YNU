# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述：创建和删除失物招领关注的信息表文件， 关注/取消关注
# 主要模块： 1.  create_table()
#          2.  drop_table()
#          3.  add_attention()
#          4.  del_attention()
#          5.  query_attention_one()
#          6.  query_attention_object_size()
#          7.  query_attention_by_object()
#          8.  query_attention_by_user()
#
# 作者: 方成
# 单位： 云南大学信息学院
# 生成日期：2020-10-27
# ----------------------------------------------------------------------------- #
import config
import logging
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, and_, func
from utils import RESULT_ERROR, RESULT_OK, RESULT_FAILED, get_session

# 生成ORM基类
Base = declarative_base()


class Attention(Base):
    """
    关注信息表
    """
    __tablename__ = "attention_info"                                    # 表名
    ID = Column(Integer, primary_key=True, autoincrement=True)          # 自增编号
    OPEN_ID = Column(String(128), nullable=False)                       # 微信用户的openid
    OBJECT_ID = Column(String(128), nullable=False)                     # 丢失物的ID
    DATE_TIME = Column(DateTime, nullable=False)                        # 时间日期

    def __init__(self, user_id, obj_id, date_time):
        self.OPEN_ID = user_id
        self.OBJECT_ID = obj_id
        self.DATE_TIME = date_time


def create_table():
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL, encoding=config.DB_ENCODE)
        # 执行创建表结构
        Base.metadata.create_all(engine)
        logging.info('OK: attention.py--->create_table() 成功！')
        return RESULT_OK
    except Exception as e:
        print(e)
        logging.critical('ERROR: attention.py--->create_table() 失败！ {0}'.format(e))
        return RESULT_FAILED


def drop_table():
    try:
        # 连接数据库，echo=True =>把所有的信息都打印出来
        engine = create_engine(config.DB_URL)  # , echo=True
        # 执行创建表结构
        Base.metadata.drop_all(engine)
        logging.info('OK: attention.py--->drop_table() 成功！')
        return RESULT_OK
    except Exception as e:
        logging.critical('ERROR: attention.py--->drop_table() 失败！ {0}'.format(e))
        return RESULT_FAILED


def add_attention(**kwargs):
    """
    新增一条关注
    :param kwargs: {'user_id': user_id, 'object_id': object_id}
    :return:
    """
    session = None
    try:
        session = get_session()
        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 查询是否已经被指定的用户关注过；
        # 如果已经关注过，直接返回
        num = session.query(func.count('*')).filter(and_(Attention.OPEN_ID == kwargs['user_id'],
                                                         Attention.OBJECT_ID == kwargs['object_id'])).scalar()
        if num == 0:
            new_attention = Attention(user_id=kwargs['user_id'],
                                      obj_id=kwargs['object_id'],
                                      date_time=_time)

            # 全部添加到session
            session.add(new_attention)
            # 提交即保存到数据库
            session.commit()
            logging.info('OK : attention.py--->add_attention(), 成功')
        return RESULT_OK
    except Exception as e:
        # 出错时，回滚一下
        session.rollback()
        logging.critical('ERROR: attention.py--->add_attention() 关注失败！ {0}'.format(e))
        return RESULT_FAILED
    finally:
        session.close()


def del_attention(**kwargs):
    """
    按照用户ID 与 OBJ_ID 删除发布的丢失信息，两个条件同时满足才能执行删除操作
    :param kwargs: {'user_id': user_id, 'obj_id' : obj_id}
    :return:
    """
    session = None
    try:
        user_id, obj_id = kwargs['user_id'], kwargs['object_id']
        session = get_session()
        session.query(Attention).filter(and_(Attention.OPEN_ID == user_id,
                                             Attention.OBJECT_ID == obj_id)).delete()
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : attention.py--->add_attention() 成功')
        return RESULT_OK
    except Exception as e:
        session.rollback()
        logging.critical('Error : lost_table.py--->del_data() 失败 : {}'.format(e))
        return RESULT_ERROR
    finally:
        # 关闭session
        session.close()


def query_attention_by_user(**kwargs):
    """
    查询当前用户关注的所有物件
    :param kwargs: {'user_id': user_id}
    :return: obj_id
    """
    session = None
    try:
        session = get_session()
        result = session.query(Attention).filter(Attention.OPEN_ID == kwargs['user_id']).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = []
        for _result in result:
            results.append({'OPEN_ID': _result.OPEN_ID, 'OBJECT_ID': _result.OBJECT_ID})

        logging.info('OK : attention.py--->query_attention_by_user(), 成功')
        return results
    except Exception as e:
        logging.critical('Error : attention.py--->query_attention_by_user() 失败:{}'.format(e))
        return []
    finally:
        session.close()


def query_attention_by_object(**kwargs):
    """
    查询当 object_id 被哪些用户关注
    :param kwargs: {'object_id': object_id}
    :return:
    """
    session = None
    try:
        session = get_session()
        result = session.query(Attention).filter(
                               Attention.OBJECT_ID == kwargs['object_id']).limit(config.LIMIT_MAX).all()
        # 提交即保存到数据库
        session.commit()
        results = []
        for _result in result:
            results.append({'OPEN_ID': _result.OPEN_ID, 'OBJECT_ID': _result.OBJECT_ID})

        logging.info('OK : attention.py--->query_attention_by_object() 成功')
        return results
    except Exception as e:
        logging.critical('Error : attention.py--->query_attention_by_object() 失败:{0}'.format(e))
        return []
    finally:
        session.close()


def query_attention_object_size(**kwargs):
    """
    查询物品被关注的数量
    :param kwargs: {'object_id': object_id}
    :return: number
    """
    session = None
    try:
        session = get_session()
        num = session.query(func.count('*')).filter(Attention.OBJECT_ID == kwargs['object_id']).scalar()
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : attention.py--->query_attention() 成功')
        return str(num)
    except Exception as e:
        logging.critical('Error : attention.py--->query_attention() 失败: {0}'.format(e))
        return RESULT_ERROR
    finally:
        # 关闭session
        session.close()


def query_attention_one(**kwargs):
    """
    查询当前用户是否关注指定的物件
    :param kwargs: {'user_id': user_id, 'object_id': object_id}
    :return: 0 or 1
    """
    session = None
    try:
        session = get_session()
        results = session.query(func.count('*')).filter(and_(Attention.OPEN_ID == kwargs['user_id'],
                                                        Attention.OBJECT_ID == kwargs['object_id'])).scalar()
        # 提交即保存到数据库
        session.commit()
        logging.info('OK : attention.py--->query_attention_one(), 成功')
        return str(results)
    except Exception as e:
        logging.critical('Error : attention.py--->query_attention_one() 失败:{}'.format(e))
        return RESULT_ERROR
    finally:
        session.close()


if __name__ == '__main__':
    # o7C2I5e-rhXE1Fpbru9f1_w_OM1U
    # o7C2I5IZorGbj84FkojkGY7TqTeI
    # drop_table()
    create_table()
    # add_attention({'user_id': '0', 'object_id': '123456.'})
    # del_attention({'user_id': '10', 'object_id': '123456/'})
    # res = query_attention_one({'user_id': '1', 'object_id': '123456*'})
    # res = query_attention_object_size({'object_id': '123456*'})
    # res = query_attention_by_user({'user_id': '3'})
    # res = query_attention_one(**{'user_id': '4', 'obj_id': 'obj_9205#45'})

