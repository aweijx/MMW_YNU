# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述：通用的不见
# 主要模块：
#
# 作者: 方成
# 单位： 云南大学信息学院
# 生成日期：2020-11-10
# ----------------------------------------------------------------------------- #
import os
import math
import random
import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# 函数返回值定义
RESULT_OK = 'ok'
RESULT_FAILED = 'failed'
RESULT_ERROR = 'error'


def gen_object_id(user_id=None, object_class='found'):
    """
    随机生成 OBJECT_ID
    :param user_id:  用户ID
    :param object_class:  目标类别， found, study, play, second
    :return:
    """
    # 生成6位随机数
    nums = math.floor(1e6 * random.random())
    if user_id is None or '' == user_id:
        return '{0}_{1}_'.format(object_class, str(nums))

    return '{0}_{1}_{2}'.format(object_class, str(nums), user_id)


def get_session():
    """
    初始化数据库连接
    :return: session
    """
    engine = create_engine(config.DB_URL, encoding=config.DB_ENCODE)
    session = sessionmaker(bind=engine)
    return session()
