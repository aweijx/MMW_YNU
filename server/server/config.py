# -*- coding: utf-8 -*-
import os

# -------------- 云端MySQL数据库 ------------- #
# 数据库名
DB_NAME = 'wx'
# 数据库连接名
HOST_NAME = 'root'
# 数据库密码
DB_PWD = 'fc2020.'

# 打开配置文件
with open("config.txt", "r") as f:
    SERVER = f.readline().strip('\n')  # 去掉列表中每一个元素的换行符

# 数据库连接字符串
DB_URL = "mysql+pymysql://{}:{}@{}/{}".format(HOST_NAME, DB_PWD, SERVER, DB_NAME)
DB_ENCODE = "utf-8"

# ----------------- 日志 --------------- #
# 日志开关
LOG_ON = True
# 日志路径
LOG_PATH = '/mnt/wx/logs'
# 日志名称
LOG_NAME = 'my.log'
# 日志格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# 日志的时间格式
DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"

# -------------- 服务器配置 ------------- #
# 服务器图像文件存放路径
SERVER_IMAGE_DIR = "/mnt/www.miaomiaowu.com/"
# 服务器页面路径
SERVER_DIR = "/mnt/www.miaomiaowu.com/"

# --------------- 生成OBJ_ID的位数 ----------- #
OBJ_ID_SIZE = 5

# --------------- 查询最大返回记录数 ----------- #
LIMIT_MAX = 100
PAGE_SIZE = 30  # 每次页面刷新请求得到的数据数

# ------------------------------------------- #
INIT_FOUND_STUTAS = '没找到'
INIT_SECOND_HAND_STUTAS = '没卖'

# ------------------------------------------- #
INIT_SERVER = True
INIT_SERVER_METHOD = 'remain'

# ------------------------------------------- #
BEGIN_DAY_TIME = ' 0:0:0'
END_DAY_TIME = ' 23:59:59'

# ------------ version ----------------------- #
VERSION = 'v1.0.5'
DATE_SUMBIT = '2020-06-19'


# ---------------- develop logs --------------- #
# 2020-06-13
# 1.修改了查询结果的 MSG_CNT 的取值，之前是靠新增的时候主动去更新found,play,study,second_hand 中 MSG_CNT 的值，这种会出问题，现在修改成再
# 查询的时候主动取统计每个object_id的留言数量。
# 2. 修改了query_attention_by_user接口，之前是返回 object_id，现在返回的是具体的记录；

# 2020-06-14
# 1.删除留言分组的第一条后，要将整个留言组的留言信息都删除；
# 2. 配置Mysql的主从同步成功； 但是Mysql-proxy还没有完成；

# 2020-06-15
# 1.搞定Mysql-proxy；3台主机实现联机运行
# 其中， MySQL Master:124.70.144.48,  MySQL Slave: 124.70.136.36
# MySQL-proxy, Nginx, Gunicorn, Flask和后台代码运行在 ： 124.70.138.101
#

# 2020-06-17
# 1. 添加了4个新的模块， 考研资讯，菜鸟编程，竞赛信息，论文
# 2. 多张图像上传的问题

# 2020-06-18
# 1.搞定多图上传
# 2.修改除查询以外的函数的返回值的结构，原因是前端认为微信上传图像的接口解析不到字典内容。
