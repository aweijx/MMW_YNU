# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述：初始化服务器
# 主要模块： 创建表文件
#
# 作者: 方成
# 单位： 云南大学信息学院
# 生成日期：2020-10-23
# 修改日期：2020-11-10
# ----------------------------------------------------------------------------- #
import os
import logging
import config
from found import found
from play import play
from second_hand import second_hand
from study import study
from coding import coding
from papers import papers
from postgraduate import postgraduate
from contest import contest

import users
import attention
import message
import banner


class Initialization(object):
    """
    初始化服务器， method='retain'，保持现有的数据；
                method='clear'，清除现有的数据；
    """

    def __init__(self, method='clear'):
        self.method = method
        self.initialize_log()
        self.initialize_tables()

    def initialize_log(self):
        """
        初始化日志
        """
        log_path = os.path.join(config.LOG_PATH, config.LOG_NAME).strip()
        # 目录是否存在
        existed = os.path.exists(config.LOG_PATH)
        # 目录不存在，就新建一个
        if not existed:
            os.makedirs(config.LOG_PATH)

        # 文件是否存在
        existed = os.path.exists(log_path)
        # 存在就将其删除掉
        if existed:
            os.remove(log_path)
        # 初始化log，配置
        logging.basicConfig(filename=os.path.join(config.LOG_PATH, config.LOG_NAME),
                            level=logging.DEBUG,
                            format=config.LOG_FORMAT,
                            datefmt=config.DATE_FORMAT)

    def initialize_tables(self):
        """
        初始化数据库表
        """
        if 'clear' == self.method:  # clear模式下，如果表文件存在，则将其删除，再重建表
            logging.info('初始化数据库表文件：init.py initialize_tables, 模式: 完全清除。')
            users.drop_table()
            users.create_table()

            coding.drop_table()
            coding.create_table()

            papers.drop_table()
            papers.create_table()

            postgraduate.drop_table()
            postgraduate.create_table()

            contest.drop_table()
            contest.create_table()

            found.drop_table()
            found.create_table()

            message.drop_table()
            message.create_table()

            attention.drop_table()
            attention.create_table()

            play.drop_table()
            play.create_table()

            second_hand.drop_table()
            second_hand.create_table()

            study.drop_table()
            study.create_table()
            logging.info('初始化数据库表文件：init.py initialize_tables, 模式: 完全清除 完成。')
        elif 'remain' == self.method:
            users.create_table()
            found.create_table()
            message.create_table()
            attention.create_table()
            play.create_table()
            study.create_table()
            message.create_table()
            banner.create_table()
            contest.create_table()
            papers.create_table()
            coding.create_table()
            postgraduate.create_table()
            logging.info('初始化数据库表文件：init.py initialize_tables, 模式: 保留数据 完成。')


if __name__ == '__main__':
    Initialization()
