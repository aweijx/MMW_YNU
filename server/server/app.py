# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述：服务主入口
# 主要模块： 1.  轮播图信息
#          2.  最新发布信息
#          3.  用户信息
#          4.  失物招领信息
#          5.  二手闲置信息
#          6.  相约学习
#          7.  约个球
#          8.  菜鸟编程
#          9.  论文推荐
#          10. 考研资讯
#          11. 竞赛信息
#          12. 留言
#          13. 关注
#
#
# 作者: 方成
# 单位： 云南大学信息学院
# 生成日期：2020-10-25
# ----------------------------------------------------------------------------- #
from flask import Flask, request, json
import config
import utils
import init
import users
import attention
import message
import banner
import common
from found import found
from study import study
from play import play
from second_hand import second_hand
from coding import coding
from papers import papers
from postgraduate import postgraduate
from contest import contest

# 使用flask框架
app = Flask(__name__)

# ---------------------------- 初始化服务器 ---------------------------------- #
if config.INIT_SERVER and False:
    init.Initialization(config.INIT_SERVER_METHOD)


# -------------------------------------------------------------------------- #
@app.route('/competition', methods=['POST', 'GET'])
def competition():
    return 'Tencent wechat Competition Winners!'


# -------------------------------------------- 1. 查询轮播图信息 ------------------------------------------------- #
@app.route('/add_banner_info', methods=['POST'])
def add_banner_info():
    """
    添加轮播图
    :return: {'result': result}
    """
    # 接收图像
    image = request.files.get('files')
    # 保存到数据库中的图像名
    file_path = ''
    if image is not None:
        # 图片path和名称组成图片的保存路径
        file_path = image.filename
        # 保存图像
        image.save(config.SERVER_IMAGE_DIR + image.filename)

    result = banner.insert_data(**{'img_url': file_path})
    return json.dumps({'result': result})


@app.route('/del_banner_info', methods=['POST'])
def del_banner_info():
    """
    删除轮播图，按照轮波图的名称进行删除
    :return: {'result': result}
    """
    img_url = request.values.get('img_url')

    result = utils.RESULT_FAILED
    if img_url is not None:
        result = banner.del_data(**{'img_url': img_url})

    return json.dumps(result)


@app.route('/query_banner_info', methods=['POST'])
def query_banner_info():
    """
    查询轮播图
    :return: {'result': result}
    """
    result = banner.query_data()
    return json.dumps({'result': result})


# -------------------------------------------- 2. 查询最新信息 ------------------------------------------------- #
@app.route('/query_latest_info', methods=['POST'])
def query_latest_info():
    """
    查询所有信息里面的最新发布信息，按时间排序
    :return: {'result': result}
    """
    # 每个页面的信息,  page_index 从0开始， 默认的每次刷新得到 30 条数据，在配置文件config.py中进行设置
    page_index = request.values.get('page_index')

    result = common.get_latest_info(page_index=page_index)
    # 给结果添加留言数 MSG_CNT
    res = message.query_msg_cnt_by_obj(*result)
    return json.dumps({'result': res})


@app.route('/query_latest_by_user', methods=['POST'])
def query_latest_by_user():
    """
    查询指定用户的最新发布信息
    :return: {'result': result}
    """
    # 每个页面的信息,  page_index 从0开始， 默认的每次刷新得到 30 条数据，在配置文件config.py中进行设置
    user_id = request.values.get('openid')
    page_index = request.values.get('page_index')

    # 查询条件不准确，直接返回空
    if user_id is None:
        return json.dumps({'result': []})

    if page_index is None:
        page_index = 0

    condition = {'user_id': user_id, 'page_index': page_index}
    result = common.get_latest_by_user(**condition)
    # 给结果添加留言数 MSG_CNT
    res = message.query_msg_cnt_by_obj(*result)
    return json.dumps({'result': res})

# -------------------------------------------- 3. 用户信息 ------------------------------------------------- #
@app.route('/add_user_info', methods=['POST'])
def add_user_info():
    """
    添加用户信息，第一次使用小程序时，做记录
    :return: {'result': result}
    """
    user_id = request.values.get('openid')
    nick_name = request.values.get('nick_name')
    gender = request.values.get('gender')
    phone = request.values.get('phone')

    result = utils.RESULT_FAILED
    if user_id is not None:
        user = {'user_id': user_id,
                'nick_name': nick_name,
                'phone': phone,
                'gender': gender}
        result = users.insert_data(**user)

    return json.dumps(result)


# 用户查询
@app.route('/query_user_info', methods=['POST'])
def query_user_info():
    """
    根据openid查询用户信息
    :return: {'result': result}
    """
    user_id = request.values.get('openid')

    result = utils.RESULT_FAILED
    if user_id is not None:
        condition = {'user_id': user_id}
        result = users.query_data(**condition)

    return json.dumps({'result': result})


# -------------------------------------------- 4. 失物招领信息 ------------------------------------------------- #
@app.route('/add_found_info', methods=['POST', 'GET'])
def add_found_info():
    """
    # 发布招领信息
    :return: {'result': result}
    """
    user_id = request.values.get('openid')
    object_name = request.values.get('object_name')
    object_class = request.values.get('object_class')
    msg = request.values.get('msg')
    phone = request.values.get('phone')
    grade = request.values.get('grade')
    major = request.values.get('major')
    gender = request.values.get('gender')
    nick_name = request.values.get('nick_name')
    # next_image 用来解决多图上传的问题，这里如果接收到的是'first'，表示这是第一张图，
    # 否则，为多图上传情况，接收到的是object_id
    next_image = request.values.get('next_image')

    result = utils.RESULT_FAILED
    if user_id is not None:
        # 保存到数据库中的图像名
        file_path = ''
        # 接收图像
        image = request.files.get('files')
        if image is not None:
            # 图片path和名称组成图片的保存路径
            file_path = image.filename
            # 保存图像
            image.save(config.SERVER_IMAGE_DIR + image.filename)

        condition = {'user_id': user_id,
                     'object_name': object_name,
                     'object_class': object_class,
                     'img_url': file_path,
                     'next_image': next_image,
                     'msg': msg,
                     'phone': phone,
                     'grade': grade,
                     'major': major,
                     'nick_name': nick_name,
                     'gender': gender}
        result = found.insert_data(**condition)

    return json.dumps(result)


@app.route('/del_found_info', methods=['POST'])
def del_found_info():
    """
    # 删除招领信息
    :return: {'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id,
                     'object_id': object_id}
        result = found.del_data(**condition)

    return json.dumps(result)


@app.route('/update_found_status', methods=['POST'])
def update_found_status():
    """
    更新招领物件的状态，只有发布信息的人才能操作
    :return: {'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')
    object_status = request.values.get('object_status')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None and object_status is not None:
        condition = {'user_id': user_id,
                     'object_id': object_id,
                     'object_status': object_status}
        result = found.update_status(**condition)

    return json.dumps(result)


@app.route('/update_found_forward', methods=['POST'])
def update_found_forward():
    """
    更新招转发量
    :return: {'result': result}
    """
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if object_id is not None:
        condition = {'object_id': object_id.strip()}
        result = found.update_forward_cnt(**condition)

    return json.dumps(result)


@app.route('/query_found_info', methods=['POST'])
def query_found_info():
    # 查询招领物件信息
    # 查询条件：
    # openid: 根据用户的openid来查询
    # object_name: 根据物件的米名称进行模糊查询
    # object_class: 根据物件的类别进行查询
    # seen_count: 根据被查看的次数
    # forward_count：根据被转发的次数
    # date_time_before: 根据时间日期进行查询，查询当前时间之前的记录，eg: 2020-06-04之前的
    # date_time_after: 根据时间日期进行查询，查询当前时间之后的记录，eg: 2020-06-04之后的
    # date_time_between: 根据时间日期进行查询，查询当前时间之间的记录，eg: 2020-06-01与2020-06-04之间的
    condition = request.values.get('condition')
    # 与查询条件对应的值
    obj_value = request.values.get('value')

    result = []
    if 'openid' == condition:
        result = found.query_by_user_id(**{'user_id': obj_value})
    elif 'object_id' == condition:
        result = found.query_by_found_id(**{'object_id': obj_value})
        # 更新被查看的次数，加1
        found.update_seen_cnt(**{'object_id': obj_value})
    elif 'object_name' == condition:
        result = found.query_by_name(**{'object_name': obj_value})
    elif 'object_class' == condition:
        result = found.query_by_class(**{'object_class': obj_value})
    elif 'seen_count' == condition:
        result = found.query_by_seen()
    elif 'forward_count' == condition:
        result = found.query_by_forward()
    elif 'date_time_before' == condition:
        result = found.query_by_date_before(**{'date': obj_value})
    elif 'date_time_after' == condition:
        result = found.query_by_date_after(**{'date': obj_value})
    elif 'date_time_between' == condition:
        result = found.query_by_date_between(**{'date': obj_value})
    # 给结果添加留言数 MSG_CNT
    res = message.query_msg_cnt_by_obj(*result)
    return json.dumps({'result': res})


# -------------------------------------------- 5. 二手闲置信息 ------------------------------------------------- #
@app.route('/add_second_hand_info', methods=['POST'])
def add_second_hand_info():
    """
    # 发布二手信息
    :return: {'result': result}
    """
    user_id = request.values.get('openid')  # 用户微信openid
    object_name = request.values.get('object_name')  # 二手货的名称
    object_class = request.values.get('object_class')  # 二手货类别
    msg = request.values.get('msg')  # 附加描述
    phone = request.values.get('phone')  # 联系电话
    grade = request.values.get('grade')  # 年级
    major = request.values.get('major')  # 专业
    gender = request.values.get('gender')  # 性别
    nick_name = request.values.get('nick_name')  # 昵称
    next_image = request.values.get('next_image')  # 是否连续传图

    result = utils.RESULT_FAILED
    if user_id is not None and '' != user_id:  # 用户id不能为空
        # 保存到数据库中的图像名
        file_path = ''
        # 接收图像
        image = request.files.get('files')
        if image is not None:
            # 图片path和名称组成图片的保存路径
            file_path = image.filename
            # 保存图像
            image.save(config.SERVER_IMAGE_DIR + image.filename)

        condition = {'user_id': user_id.strip(),
                     'object_name': object_name,
                     'object_class': object_class,
                     'img_url': file_path,
                     'msg': msg,
                     'phone': phone,
                     'next_image': next_image,
                     'grade': grade,
                     'major': major,
                     'nick_name': nick_name,
                     'gender': gender}
        result = second_hand.insert_data(**condition)

    return json.dumps(result)


@app.route('/del_second_hand_info', methods=['POST'])
def del_second_hand_info():
    """
    # 删除招领信息
    :return: {'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id, 'object_id': object_id}
        result = second_hand.del_data(**condition)

    return json.dumps(result)


@app.route('/update_second_hand_status', methods=['POST'])
def update_second_hand_status():
    """
    更新闲置二手信息的状态，只有发布信息的人才能操作
    :return: {'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')
    object_status = request.values.get('object_status')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None and object_status is not None:
        condition = {'user_id': user_id,
                     'object_id': object_id,
                     'object_status': object_status}
        result = second_hand.update_status(**condition)

    return json.dumps(result)


@app.route('/update_second_hand_forward', methods=['POST'])
def update_second_hand_forward():
    """
    更新招转发量
    :return: {'result': result}
    """
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if object_id is not None:
        condition = {'object_id': object_id.strip()}
        result = second_hand.update_forward_cnt(**condition)

    return json.dumps(result)


@app.route('/query_second_hand_info', methods=['POST'])
def query_second_hand_info():
    # 查询招领物件信息
    # 查询条件：
    # openid: 根据用户的openid来查询
    # object_name: 根据物件的米名称进行模糊查询
    # object_class: 根据物件的类别进行查询
    # seen_count: 根据被查看的次数
    # forward_count：根据被转发的次数
    # date_time_before: 根据时间日期进行查询，查询当前时间之前的记录，eg: 2020-06-04之前的
    # date_time_after: 根据时间日期进行查询，查询当前时间之后的记录，eg: 2020-06-04之后的
    # date_time_between: 根据时间日期进行查询，查询当前时间之间的记录，eg: 2020-06-01与2020-06-04之间的
    condition = request.values.get('condition')
    # 与查询条件对应的值
    obj_value = request.values.get('value')

    result = []
    if 'openid' == condition:
        # 按照用户查询
        result = second_hand.query_by_user_id(**{'user_id': obj_value})
    elif 'object_id' == condition:
        # 按照具体物品查询
        result = second_hand.query_by_found_id(**{'object_id': obj_value})
        # 更新被查看的次数，加1
        second_hand.update_seen_cnt(**{'object_id': obj_value})
    elif 'object_name' == condition:
        # 按照名称查询
        result = second_hand.query_by_name(**{'object_name': obj_value})
    elif 'object_class' == condition:
        # 按照类别查询
        result = second_hand.query_by_class(**{'object_class': obj_value})
    elif 'seen_count' == condition:
        # 按照被查看的次数排序返回
        result = second_hand.query_by_seen()
    elif 'forward_count' == condition:
        # 按照被转发的次数排序返回
        result = second_hand.query_by_forward()
    elif 'date_time_before' == condition:
        result = second_hand.query_by_date_before(**{'date': obj_value})
    elif 'date_time_after' == condition:
        result = second_hand.query_by_date_after(**{'date': obj_value})
    elif 'date_time_between' == condition:
        result = second_hand.query_by_date_between(**{'date': obj_value})
    # 给结果添加留言数 MSG_CNT
    res = message.query_msg_cnt_by_obj(*result)
    return json.dumps({'result': res})


# -------------------------------------------- 6. 相约学习 ------------------------------------------------- #
@app.route('/add_study_info', methods=['POST'])
def add_study_info():
    """
    添加一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')  # 用户微信openid
    subject = request.values.get('subject')  # 学习的学科
    msg = request.values.get('msg')  # 附加消息
    phone = request.values.get('phone')  # 联系电话
    grade = request.values.get('grade')  # 年级
    major = request.values.get('major')  # 专业
    gender = request.values.get('gender')  # 性别
    nick_name = request.values.get('nick_name')  # 昵称
    next_image = request.values.get('next_image')  # 是否连续传图

    result = utils.RESULT_FAILED

    if user_id is not None:
        # 保存到数据库中的图像名
        file_path = ''
        # 接收图像
        image = request.files.get('files')
        if image is not None:
            # 图片path和名称组成图片的保存路径
            file_path = image.filename
            # 保存图像
            image.save(config.SERVER_IMAGE_DIR + image.filename)

        condition = {'user_id': user_id,
                     'subject': subject,
                     'img_url': file_path,
                     'next_image': next_image,
                     'msg': msg, 'phone': phone,
                     'grade': grade, 'major': major,
                     'nick_name': nick_name,
                     'gender': gender}
        result = study.insert_data(**condition)

    return json.dumps(result)


@app.route('/del_study_info', methods=['POST'])
def del_study_info():
    """
    删除一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id,
                     'object_id': object_id}
        result = study.del_data(**condition)

    return json.dumps(result)


@app.route('/update_study_forward', methods=['POST'])
def update_study_forward():
    """
    新增一次转发量  {'object_id': object_id}
    :return:{'result': result}
    """
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if object_id is not None:
        condition = {'object_id': object_id}
        result = study.update_forward_cnt(**condition)

    return json.dumps(result)


@app.route('/query_study_info', methods=['POST'])
def query_study_info():
    # 查询学习信息
    # 查询条件：
    # openid: 根据用户的openid来查询
    # obj_name: 根据物件的米名称进行模糊查询
    # obj_class: 根据物件的类别进行查询
    # date_time_before: 根据时间日期进行查询，查询当前时间之前的记录，eg: 2020-06-04之前的
    # date_time_after: 根据时间日期进行查询，查询当前时间之后的记录，eg: 2020-06-04之后的
    # date_time_between: 根据时间日期进行查询，查询当前时间之间的记录，eg: 2020-06-01与2020-06-04之间的
    condition = request.values.get('condition')
    # 与查询条件对应的值
    obj_value = request.values.get('value')

    result = []
    if 'openid' == condition:
        result = study.query_by_user_id(**{'user_id': obj_value})
    elif 'object_id' == condition:
        # 按照学习信息的ID查询，返回一条具体详情
        result = study.query_by_study_id(**{'object_id': obj_value})
        # 更新被查看的次数，加1
        study.update_seen_cnt(**{'object_id': obj_value})
    elif 'object_name' == condition:
        # 按科目查询
        result = study.query_by_subject(**{'subject': obj_value})
    elif 'seen_count' == condition:
        # 按照被查看次数的降序返回
        result = study.query_by_seen()
    elif 'forward_count' == condition:
        # 按照被转发次数的降序返回
        result = study.query_by_forward()
    elif 'date_time_before' == condition:
        result = study.query_by_date_before(**{'date': obj_value})
    elif 'date_time_after' == condition:
        result = study.query_by_date_after(**{'date': obj_value})
    elif 'date_time_between' == condition:
        result = study.query_by_date_between(**{'date': obj_value})
    # 给结果添加留言数 MSG_CNT
    res = message.query_msg_cnt_by_obj(*result)
    return json.dumps({'result': res})


# -------------------------------------------- 7.约个球 ------------------------------------------------- #
@app.route('/add_play_info', methods=['POST'])
def add_play_info():
    """
    添加一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')  # 用户微信openid
    subject = request.values.get('subject')  # 玩什么类别的球，羽毛球，篮球，乒乓球，等
    msg = request.values.get('msg')  # 附加消息
    phone = request.values.get('phone')  # 联系电话
    grade = request.values.get('grade')  # 年级
    major = request.values.get('major')  # 专业
    gender = request.values.get('gender')  # 性别
    nick_name = request.values.get('nick_name')  # 昵称
    next_image = request.values.get('next_image')  # 是否连续传图

    result = utils.RESULT_FAILED
    if user_id is not None:
        # 保存到数据库中的图像名
        file_path = ''
        # 接收图像
        image = request.files.get('files')
        if image is not None:
            # 图片path和名称组成图片的保存路径
            file_path = image.filename
            # 保存图像
            image.save(config.SERVER_IMAGE_DIR + image.filename)

        condition = {'user_id': user_id,
                     'subject': subject,
                     'img_url': file_path,
                     'next_image': next_image,
                     'msg': msg, 'phone': phone,
                     'grade': grade, 'major': major,
                     'nick_name': nick_name,
                     'gender': gender}
        result = play.insert_data(**condition)

    return json.dumps(result)


@app.route('/del_play_info', methods=['POST'])
def del_play_info():
    """
    删除一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id.strip(),
                     'object_id': object_id.strip()}
        result = play.del_data(**condition)

    return json.dumps(result)


@app.route('/update_play_forward', methods=['POST'])
def update_play_forward():
    """
    新增一次转发量  {'object_id': object_id}
    :return:{'result': result}
    """
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if object_id is not None:
        condition = {'object_id': object_id.strip()}
        result = play.update_forward_cnt(**condition)

    return json.dumps(result)


@app.route('/query_play_info', methods=['POST'])
def query_play_info():
    # 查询约打球信息
    # 查询条件：
    # openid: 根据用户的openid来查询
    # obj_name: 根据名称进行模糊查询
    # obj_class: 根据类别进行查询
    # date_time_before: 根据时间日期进行查询，查询当前时间之前的记录，eg: 2020-06-04之前的
    # date_time_after: 根据时间日期进行查询，查询当前时间之后的记录，eg: 2020-06-04之后的
    # date_time_between: 根据时间日期进行查询，查询当前时间之间的记录，eg: 2020-06-01与2020-06-04之间的
    condition = request.values.get('condition')
    # 与查询条件对应的值
    obj_value = request.values.get('value')

    result = []
    if 'openid' == condition:
        result = play.query_by_user_id(**{'user_id': obj_value})
    elif 'object_id' == condition:
        # 按照信息的ID查询，返回一条具体详情
        result = play.query_by_study_id(**{'object_id': obj_value})
        # 更新被查看的次数，加1
        play.update_seen_cnt(**{'object_id': obj_value})
    elif 'object_name' == condition:
        # 按科目查询
        result = play.query_by_subject(**{'subject': obj_value})
    elif 'seen_count' == condition:
        # 按照被查看次数的降序返回
        result = play.query_by_seen()
    elif 'forward_count' == condition:
        # 按照被转发次数的降序返回
        result = play.query_by_forward()
    elif 'date_time_before' == condition:
        result = play.query_by_date_before(**{'date': obj_value})
    elif 'date_time_after' == condition:
        result = play.query_by_date_after(**{'date': obj_value})
    elif 'date_time_between' == condition:
        result = play.query_by_date_between(**{'date': obj_value})
    # 给结果添加留言数 MSG_CNT
    res = message.query_msg_cnt_by_obj(*result)
    return json.dumps({'result': res})


# -------------------------------------------- 8.菜鸟编程 ------------------------------------------------- #
@app.route('/add_code_info', methods=['POST'])
def add_code_info():
    """
    添加一条菜鸟编程信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')  # 用户微信openid
    subject = request.values.get('subject')  # 哪种语言，C/C++, Python, Java,等
    msg = request.values.get('msg')  # 附加消息
    phone = request.values.get('phone')  # 联系电话
    grade = request.values.get('grade')  # 年级
    major = request.values.get('major')  # 专业
    gender = request.values.get('gender')  # 性别
    nick_name = request.values.get('nick_name')  # 昵称
    next_image = request.values.get('next_image')  # 是否连续传图

    result = utils.RESULT_FAILED
    if user_id is not None:
        # 保存到数据库中的图像名
        file_path = ''
        # 接收图像
        image = request.files.get('files')
        if image is not None:
            # 图片path和名称组成图片的保存路径
            file_path = image.filename
            # 保存图像
            image.save(config.SERVER_IMAGE_DIR + image.filename)

        condition = {'user_id': user_id,
                     'subject': subject,
                     'img_url': file_path,
                     'next_image': next_image,
                     'msg': msg, 'phone': phone,
                     'grade': grade, 'major': major,
                     'nick_name': nick_name,
                     'gender': gender}
        result = coding.insert_data(**condition)

    return json.dumps(result)


@app.route('/del_code_info', methods=['POST'])
def del_code_info():
    """
    删除一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id, 'object_id': object_id}
        result = coding.del_data(**condition)

    return json.dumps(result)


@app.route('/update_code_forward', methods=['POST'])
def update_code_forward():
    """
    新增一次转发量  {'object_id': object_id}
    :return:{'result': result}
    """
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if object_id is not None:
        condition = {'object_id': object_id.strip()}
        result = coding.update_forward_cnt(**condition)

    return json.dumps(result)


@app.route('/query_code_info', methods=['POST'])
def query_code_info():
    # 查询约打球信息
    # 查询条件：
    # openid: 根据用户的openid来查询
    # obj_name: 根据名称进行模糊查询
    # obj_class: 根据类别进行查询
    # date_time_before: 根据时间日期进行查询，查询当前时间之前的记录，eg: 2020-06-04之前的
    # date_time_after: 根据时间日期进行查询，查询当前时间之后的记录，eg: 2020-06-04之后的
    # date_time_between: 根据时间日期进行查询，查询当前时间之间的记录，eg: 2020-06-01与2020-06-04之间的
    condition = request.values.get('condition')
    # 与查询条件对应的值
    obj_value = request.values.get('value')

    result = []
    if 'openid' == condition:
        result = coding.query_by_user_id(**{'user_id': obj_value})
    elif 'object_id' == condition:
        # 按照信息的ID查询，返回一条具体详情
        result = coding.query_by_study_id(**{'object_id': obj_value})
        # 更新被查看的次数，加1
        coding.update_seen_cnt(**{'object_id': obj_value})
    elif 'object_name' == condition:
        # 按科目查询
        result = coding.query_by_subject(**{'subject': obj_value})
    elif 'seen_count' == condition:
        # 按照被查看次数的降序返回
        result = coding.query_by_seen()
    elif 'forward_count' == condition:
        # 按照被转发次数的降序返回
        result = coding.query_by_forward()
    elif 'date_time_before' == condition:
        result = coding.query_by_date_before(**{'date': obj_value})
    elif 'date_time_after' == condition:
        result = coding.query_by_date_after(**{'date': obj_value})
    elif 'date_time_between' == condition:
        result = coding.query_by_date_between(**{'date': obj_value})
    # 给结果添加留言数 MSG_CNT
    res = message.query_msg_cnt_by_obj(*result)
    return json.dumps({'result': res})


# -------------------------------------------- 9.论文推荐 ------------------------------------------------- #
@app.route('/add_paper_info', methods=['POST'])
def add_paper_info():
    """
    添加一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')  # 用户微信openid
    subject = request.values.get('subject')  # 论文研究的方向
    msg = request.values.get('msg')  # 附加消息
    phone = request.values.get('phone')  # 联系电话
    grade = request.values.get('grade')  # 年级
    major = request.values.get('major')  # 专业
    gender = request.values.get('gender')  # 性别
    nick_name = request.values.get('nick_name')  # 昵称
    next_image = request.values.get('next_image')  # 是否连续传图

    result = utils.RESULT_FAILED
    if user_id is not None:
        # 保存到数据库中的图像名
        file_path = ''
        # 接收图像
        image = request.files.get('files')
        if image is not None:
            # 图片path和名称组成图片的保存路径
            file_path = image.filename
            # 保存图像
            image.save(config.SERVER_IMAGE_DIR + image.filename)

        condition = {'user_id': user_id,
                     'subject': subject,
                     'img_url': file_path,
                     'next_image': next_image,
                     'msg': msg, 'phone': phone,
                     'grade': grade, 'major': major,
                     'nick_name': nick_name,
                     'gender': gender}
        result = papers.insert_data(**condition)

    return json.dumps(result)


@app.route('/del_paper_info', methods=['POST'])
def del_paper_info():
    """
    删除一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id.strip(),
                     'object_id': object_id.strip()}
        result = papers.del_data(**condition)

    return json.dumps(result)


@app.route('/update_papers_forward', methods=['POST'])
def update_paper_forward():
    """
    新增一次转发量  {'object_id': object_id}
    :return:{'result': result}
    """
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if object_id is None:
        condition = {'object_id': object_id}
        result = papers.update_forward_cnt(**condition)

    return json.dumps(result)


@app.route('/query_paper_info', methods=['POST'])
def query_paper_info():
    # 查询约打球信息
    # 查询条件：
    # openid: 根据用户的openid来查询
    # obj_name: 根据名称进行模糊查询
    # obj_class: 根据类别进行查询
    # date_time_before: 根据时间日期进行查询，查询当前时间之前的记录，eg: 2020-06-04之前的
    # date_time_after: 根据时间日期进行查询，查询当前时间之后的记录，eg: 2020-06-04之后的
    # date_time_between: 根据时间日期进行查询，查询当前时间之间的记录，eg: 2020-06-01与2020-06-04之间的
    condition = request.values.get('condition')
    # 与查询条件对应的值
    obj_value = request.values.get('value')

    result = []
    if 'openid' == condition:
        result = papers.query_by_user_id(**{'user_id': obj_value})
    elif 'object_id' == condition:
        # 按照信息的ID查询，返回一条具体详情
        result = papers.query_by_study_id(**{'object_id': obj_value})
        # 更新被查看的次数，加1
        papers.update_seen_cnt(**{'object_id': obj_value})
    elif 'object_name' == condition:
        # 按科目查询
        result = papers.query_by_subject(**{'subject': obj_value})
    elif 'seen_count' == condition:
        # 按照被查看次数的降序返回
        result = papers.query_by_seen()
    elif 'forward_count' == condition:
        # 按照被转发次数的降序返回
        result = papers.query_by_forward()
    elif 'date_time_before' == condition:
        result = papers.query_by_date_before(**{'date': obj_value})
    elif 'date_time_after' == condition:
        result = papers.query_by_date_after(**{'date': obj_value})
    elif 'date_time_between' == condition:
        result = papers.query_by_date_between(**{'date': obj_value})
    # 给结果添加留言数 MSG_CNT
    res = message.query_msg_cnt_by_obj(*result)
    return json.dumps({'result': res})


# -------------------------------------------- 10.考研资讯 ------------------------------------------------- #
@app.route('/add_postgraduate_info', methods=['POST'])
def add_postgraduate_info():
    """
    添加一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')  # 用户微信openid
    subject = request.values.get('subject')  # 考研方向
    msg = request.values.get('msg')  # 附加消息
    phone = request.values.get('phone')  # 联系电话
    grade = request.values.get('grade')  # 年级
    major = request.values.get('major')  # 专业
    gender = request.values.get('gender')  # 性别
    nick_name = request.values.get('nick_name')  # 昵称
    next_image = request.values.get('next_image')  # 是否连续传图

    result = utils.RESULT_FAILED
    if user_id is not None:
        # 保存到数据库中的图像名
        file_path = ''
        # 接收图像
        image = request.files.get('files')
        if image is not None:
            # 图片path和名称组成图片的保存路径
            file_path = image.filename
            # 保存图像
            image.save(config.SERVER_IMAGE_DIR + image.filename)

        condition = {'user_id': user_id,
                     'subject': subject,
                     'img_url': file_path,
                     'next_image': next_image,
                     'msg': msg, 'phone': phone,
                     'grade': grade, 'major': major,
                     'nick_name': nick_name,
                     'gender': gender}
        result = postgraduate.insert_data(**condition)

    return json.dumps(result)


@app.route('/del_postgraduate_info', methods=['POST'])
def del_postgraduate_info():
    """
    删除一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id, 'object_id': object_id}
        result = postgraduate.del_data(**condition)

    return json.dumps(result)


@app.route('/update_postgraduate_forward', methods=['POST'])
def update_postgraduate_forward():
    """
    新增一次转发量  {'object_id': object_id}
    :return:{'result': result}
    """
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if object_id is not None:
        condition = {'object_id': object_id}
        result = postgraduate.update_forward_cnt(**condition)

    return json.dumps(result)


@app.route('/query_postgraduate_info', methods=['POST'])
def query_postgraduate_info():
    # 查询约打球信息
    # 查询条件：
    # openid: 根据用户的openid来查询
    # obj_name: 根据名称进行模糊查询
    # obj_class: 根据类别进行查询
    # date_time_before: 根据时间日期进行查询，查询当前时间之前的记录，eg: 2020-06-04之前的
    # date_time_after: 根据时间日期进行查询，查询当前时间之后的记录，eg: 2020-06-04之后的
    # date_time_between: 根据时间日期进行查询，查询当前时间之间的记录，eg: 2020-06-01与2020-06-04之间的
    condition = request.values.get('condition')
    # 与查询条件对应的值
    obj_value = request.values.get('value')

    result = []
    if 'openid' == condition:
        result = postgraduate.query_by_user_id(**{'user_id': obj_value})
    elif 'object_id' == condition:
        # 按照信息的ID查询，返回一条具体详情
        result = postgraduate.query_by_study_id(**{'object_id': obj_value})
        # 更新被查看的次数，加1
        postgraduate.update_seen_cnt(**{'object_id': obj_value})
    elif 'object_name' == condition:
        # 按科目查询
        result = postgraduate.query_by_subject(**{'subject': obj_value})
    elif 'seen_count' == condition:
        # 按照被查看次数的降序返回
        result = postgraduate.query_by_seen()
    elif 'forward_count' == condition:
        # 按照被转发次数的降序返回
        result = postgraduate.query_by_forward()
    elif 'date_time_before' == condition:
        result = postgraduate.query_by_date_before(**{'date': obj_value})
    elif 'date_time_after' == condition:
        result = postgraduate.query_by_date_after(**{'date': obj_value})
    elif 'date_time_between' == condition:
        result = postgraduate.query_by_date_between(**{'date': obj_value})
    # 给结果添加留言数 MSG_CNT
    res = message.query_msg_cnt_by_obj(*result)
    return json.dumps({'result': res})


# -------------------------------------------- 11.竞赛信息 ------------------------------------------------- #
@app.route('/add_contest_info', methods=['POST'])
def add_contest_info():
    """
    添加一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')  # 用户微信openid
    subject = request.values.get('subject')  # 竞赛学科
    msg = request.values.get('msg')  # 附加消息
    phone = request.values.get('phone')  # 联系电话
    grade = request.values.get('grade')  # 性别
    major = request.values.get('major')  # 专业
    gender = request.values.get('gender')  # 年级
    nick_name = request.values.get('nick_name')  # 昵称
    next_image = request.values.get('next_image')  # 是否连续传图

    result = utils.RESULT_FAILED
    if user_id is not None:
        file_path = ''
        image = request.files.get('files')
        if image is not None:
            # 图片path和名称组成图片的保存路径
            file_path = image.filename
            # 保存图像
            image.save(config.SERVER_IMAGE_DIR + image.filename)

        condition = {'user_id': user_id,
                     'subject': subject,
                     'img_url': file_path,
                     'next_image': next_image,
                     'msg': msg, 'phone': phone,
                     'grade': grade, 'major': major,
                     'nick_name': nick_name,
                     'gender': gender}
        result = contest.insert_data(**condition)

    return json.dumps(result)


@app.route('/del_contest_info', methods=['POST'])
def del_contest_info():
    """
    删除一条信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id, 'object_id': object_id}
        result = contest.del_data(**condition)

    return json.dumps(result)


@app.route('/update_contest_forward', methods=['POST'])
def update_contest_forward():
    """
    新增一次转发量  {'object_id': object_id}
    :return:{'result': result}
    """
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if object_id is not None:
        condition = {'object_id': object_id.strip()}
        result = contest.update_forward_cnt(**condition)

    return json.dumps(result)


@app.route('/query_contest_info', methods=['POST'])
def query_contest_info():
    # 查询约打球信息
    # 查询条件：
    # openid: 根据用户的openid来查询
    # obj_name: 根据名称进行模糊查询
    # obj_class: 根据类别进行查询
    # date_time_before: 根据时间日期进行查询，查询当前时间之前的记录，eg: 2020-06-04之前的
    # date_time_after: 根据时间日期进行查询，查询当前时间之后的记录，eg: 2020-06-04之后的
    # date_time_between: 根据时间日期进行查询，查询当前时间之间的记录，eg: 2020-06-01与2020-06-04之间的
    condition = request.values.get('condition')
    # 与查询条件对应的值
    obj_value = request.values.get('value')

    result = []
    if 'openid' == condition:
        result = contest.query_by_user_id(**{'user_id': obj_value})
    elif 'object_id' == condition:
        # 按照信息的ID查询，返回一条具体详情
        result = contest.query_by_study_id(**{'object_id': obj_value})
        # 更新被查看的次数，加1
        contest.update_seen_cnt(**{'object_id': obj_value})
    elif 'object_name' == condition:
        # 按科目查询
        result = contest.query_by_subject(**{'subject': obj_value})
    elif 'seen_count' == condition:
        # 按照被查看次数的降序返回
        result = contest.query_by_seen()
    elif 'forward_count' == condition:
        # 按照被转发次数的降序返回
        result = contest.query_by_forward()
    elif 'date_time_before' == condition:
        result = contest.query_by_date_before(**{'date': obj_value})
    elif 'date_time_after' == condition:
        result = contest.query_by_date_after(**{'date': obj_value})
    elif 'date_time_between' == condition:
        result = contest.query_by_date_between(**{'date': obj_value})
    # 给结果添加留言数 MSG_CNT
    res = message.query_msg_cnt_by_obj(*result)
    return json.dumps({'result': res})


# -------------------------------------------- 12.留言 ------------------------------------------------- #
@app.route('/add_message', methods=['POST'])
def add_message():
    """
    添加一条留言信息
    :return:{'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')
    msg = request.values.get('msg')
    nick_name = request.values.get('nick_name')
    gender = request.values.get('gender')
    target_id = request.values.get('target_id')   # 给谁留言
    group_id = request.values.get('group_id')

    result = utils.RESULT_FAILED
    # 判断能否操作
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id,
                     'object_id': object_id,
                     'msg': msg,
                     'nick_name': nick_name,
                     'target_id': target_id,
                     'group_id': group_id,
                     'gender': gender}
        result = message.insert_data(**condition)

    return json.dumps(result)


@app.route('/del_message', methods=['POST'])
def del_message():
    """
    根据openid 和 object_id 删除一条留言信息， 同一个物品，一个人可以留多条言
    :return:{'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id, 'object_id': object_id}
        result = message.del_data(**condition)

    return json.dumps(result)


@app.route('/del_by_message_id', methods=['POST'])
def del_by_message_id():
    """
    根据 object_id 和留言的 message_id 删除一条留言信息；
    input: object_id 和 message_id
    :return:{'result': result}
    """
    object_id = request.values.get('object_id')
    message_id = request.values.get('message_id')

    result = utils.RESULT_FAILED
    if message_id is not None and object_id is not None:
        condition = {'object_id': object_id, 'message_id': message_id}
        result = message.del_by_message_id(**condition)

    return json.dumps(result)


@app.route('/query_message_by_user', methods=['POST'])
def query_message_by_user():
    """
    查询openid发布的留言信息，即查询我给别人的留言
    :return: {'result': result}
    """
    user_id = request.values.get('openid')

    result = []
    if user_id is not None:
        condition = {'user_id': user_id}
        result = message.query_msg_by_user(**condition)

    return json.dumps({'result': result})


@app.route('/query_message_to_user', methods=['POST'])
def query_message_to_user():
    """
    查询别人给openid的留言信息，即查询别人给我的留言。
    date time: 2020-06-13
    :return: {'result': result}
    """
    user_id = request.values.get('openid')

    result = []
    if user_id is not None:
        condition = {'user_id': user_id}
        result = message.query_msg_to_user(**condition)

    return json.dumps({'result': result})


@app.route('/query_message_by_obj', methods=['POST'])
def query_message_by_obj():
    """
    根据 object_id 查询留言信息
    :return: {'result': result}
    """
    object_id = request.values.get('object_id')

    result = []
    if object_id is not None:
        condition = {'object_id': object_id}
        result = message.query_msg_by_obj(**condition)

    return json.dumps({'result': result})


@app.route('/query_message', methods=['POST'])
def query_message():
    """
    根据user_id 与 object_id 查询留言信息, 3种选择：
    1.当输入 openid == None & object_id ！= None 时，按照 object_id 查询,   eg: query_message(openid=None, object_id='123456')
    2.当输入 openid != None & object_id == None 时，按照 openid 查询,       eg: query_message(openid='1', object_id='None')
    3.当输入 openid != None & object_id ！= None 时，按照 openid && object_id查询
    :return: {'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = []
    if user_id is None and object_id is not None:
        # 当输入 user_id = None 且 object_id ！= None 时，按照 object_id 查询
        result = message.query_msg_by_obj(**{'object_id': object_id})
    elif object_id is None and user_id is None:
        # 当输入 object_id = None 且 openid ！= None 时，按照 openid 查询
        result = message.query_msg_by_user(**{'user_id': user_id})
    elif user_id is not None and object_id is not None:
        #  最后同时按照两个条件查询
        result = message.query_msg(**{'user_id': user_id, 'object_id': object_id})

    return json.dumps({'result': result})


# -------------------------------------------- 13.关注 ------------------------------------------------- #
@app.route('/add_attention', methods=['POST'])
def add_attention():
    """
    根据 openid 和需要关注的 object_id 添加一条关注
    :return: {'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if object_id is not None and user_id is not None:
        condition = {'user_id': user_id, 'object_id': object_id}
        result = attention.add_attention(**condition)

    return json.dumps(result)


@app.route('/del_attention', methods=['POST'])
def del_attention():
    """
    根据 openid 和需要关注的 object_id 取消关注一条关注
    :return: {'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = utils.RESULT_FAILED
    if object_id is not None and user_id is not None:
        result = attention.del_attention(**{'user_id': user_id, 'object_id': object_id})

    return json.dumps(result)


@app.route('/query_attention_by_user', methods=['POST'])
def query_attention_by_user():
    """
    查询 openid 所有关注的信息
    :return: {'result': result}
    """
    user_id = request.values.get('openid')

    result = []
    if user_id is not None:
        # result = attention.query_attention_by_user(condition)
        result = common.query_attention_by_user(**{'user_id': user_id})
    return json.dumps({'result': result})


@app.route('/query_attention_by_obj', methods=['POST'])
def query_attention_by_obj():
    """
    查询object_id关注的所有的失物招领信息
    :return: {'result': result}
    """
    object_id = request.values.get('object_id')

    result = []
    if object_id is not None:
        result = attention.query_attention_by_object(**{'object_id': object_id})

    return json.dumps({'result': result})


@app.route('/query_attention_obj_size', methods=['POST'])
def query_attention_obj_size():
    """
    查询被关注的次数
    :return: {'result': result}
    """
    object_id = request.values.get('object_id')

    result = []
    if object_id is not None:
        condition = {'object_id': object_id}
        result = attention.query_attention_object_size(**condition)

    return json.dumps({'result': result})


@app.route('/query_lost_found_attention_one', methods=['POST'])
def query_lost_found_attention_one():
    """
    查询当前用户是否关注指定的物件
    :return: 关注：'1'， 不关注：'0', {'result': result}
    """
    user_id = request.values.get('openid')
    object_id = request.values.get('object_id')

    result = []
    if user_id is not None and object_id is not None:
        condition = {'user_id': user_id, 'object_id': object_id}
        result = attention.query_attention_one(**condition)

    return json.dumps({'result': result})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
