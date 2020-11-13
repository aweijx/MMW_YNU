# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------- #
# 功能描述：通用的函数
# 主要模块：
#
# 作者: 方成
# 单位： 云南大学信息学院
# 生成日期：2020-11-03
# ----------------------------------------------------------------------------- #
import logging
import config
from found import found
from play import play
from second_hand import second_hand
from study import study
from attention import Attention
import utils
from contest import contest
from coding import coding
from postgraduate import postgraduate
from papers import papers


def parse_study(condition=None):
    """
    将相约学习的查询结果转换为字典形式
    :param condition:
    :return:
    """
    results = []
    for cond in condition:
        result = {'OPEN_ID': cond.OPEN_ID,
                  'OBJECT_ID': cond.OBJECT_ID,
                  'SUBJECT': cond.SUBJECT,
                  'IMG_URL': cond.IMG_URL,
                  'MSG': cond.MSG,
                  'GRADE': cond.GRADE,
                  'MAJOR': cond.MAJOR,
                  'SEEN_CNT': cond.SEEN_CNT,
                  'FORWARD_CNT': cond.FORWARD_CNT,
                  'MSG_CNT': cond.MSG_CNT,
                  'NICK_NAME': cond.NICK_NAME,
                  'GENDER': cond.GENDER,
                  'DATE_TIME': cond.DATE_TIME.strftime("%Y-%m-%d %H:%M:%S")}
        results.append(result)

    return results


def parse_object(condition=None):
    """
    将查询到的结果转换为需要的结构
    :param condition:
    :return:
    """
    results = []
    for cond in condition:
        if isinstance(cond, study.Study) or isinstance(cond, play.Play) \
                or isinstance(cond, papers.Papers) or isinstance(cond, contest.Contest)\
                or isinstance(cond, postgraduate.Postgraduate) or isinstance(cond, coding.Code):
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
        else:
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


def get_latest_info(**kwargs):
    """
    获取最新的信息，提供给主界面刷新。前端分页请求数据，每一页请求的数据量在config中配置
    :return:
    """
    page_index = kwargs['page_index']
    if isinstance(kwargs['page_index'], str):
        page_index = int(kwargs['page_index'])

    session = None
    try:
        session = utils.get_session()
        # 相约学习
        study_res = session.query(study.Study).order_by(
                    study.Study.DATE_TIME.desc()).all()
        # 约个球
        play_res = session.query(play.Play).order_by(
                    play.Play.DATE_TIME.desc()).all()
        # 二手闲置
        second_res = session.query(second_hand.SecondHand).order_by(
                    second_hand.SecondHand.DATE_TIME.desc()).all()
        # 失物招领
        found_res = session.query(found.Found).order_by(
                    found.Found.DATE_TIME.desc()).all()
        # 菜鸟编程
        code_res = session.query(coding.Code).order_by(
                    coding.Code.DATE_TIME.desc()).all()
        # 论文推荐
        paper_res = session.query(papers.Papers).order_by(
                    papers.Papers.DATE_TIME.desc()).all()
        # 竞赛
        contest_res = session.query(contest.Contest).order_by(
                    contest.Contest.DATE_TIME.desc()).all()
        # 考研资讯
        post_res = session.query(postgraduate.Postgraduate).order_by(
                    postgraduate.Postgraduate.DATE_TIME.desc()).all()

        # 提交即保存到数据库
        session.commit()
        ret = []
        ret.extend(parse_object(study_res))
        ret.extend(parse_object(play_res))
        ret.extend(parse_object(second_res))
        ret.extend(parse_object(found_res))
        ret.extend(parse_object(code_res))
        ret.extend(parse_object(paper_res))
        ret.extend(parse_object(contest_res))
        ret.extend(parse_object(post_res))

        # 计算每一页返回的数量
        page_start = page_index * config.PAGE_SIZE
        page_end = page_start + config.PAGE_SIZE

        # 再做一次按时间排序
        result = sorted(ret, key=lambda x: x['DATE_TIME'], reverse=True)[page_start:page_end]
        logging.info('OK : common.py--->get_latest_info() 成功')
        return result
    except Exception as e:
        session.rollback()
        logging.critical('Error : common.py--->get_latest_info()  失败 : {}'.format(e))
        return []
    finally:
        session.close()


def get_latest_by_user(**kwargs):
    """
    获取指定用户的最新信息，提供给主界面刷新。
    :return:
    """
    user_id = kwargs['user_id']
    page_index = kwargs['page_index']
    if isinstance(kwargs['page_index'], str):
        page_index = int(kwargs['page_index'])

    session = None
    try:
        session = utils.get_session()
        # 相约学习
        study_res = session.query(study.Study).filter(study.Study.OPEN_ID == user_id).order_by(
                    study.Study.DATE_TIME.desc()).all()
        # 约个球
        play_res = session.query(play.Play).filter(play.Play.OPEN_ID == user_id).order_by(
                    play.Play.DATE_TIME.desc()).all()
        # 二手闲置
        second_res = session.query(second_hand.SecondHand).filter(second_hand.SecondHand.OPEN_ID == user_id).order_by(
                    second_hand.SecondHand.DATE_TIME.desc()).all()
        # 失物招领
        found_res = session.query(found.Found).filter(found.Found.OPEN_ID == user_id).order_by(
                    found.Found.DATE_TIME.desc()).all()
        # 菜鸟编程
        code_res = session.query(coding.Code).filter(coding.Code.OPEN_ID == user_id).order_by(
                    coding.Code.DATE_TIME.desc()).all()
        # 竞赛
        contest_res = session.query(contest.Contest).filter(contest.Contest.OPEN_ID == user_id).order_by(
                    contest.Contest.DATE_TIME.desc()).all()
        # 论文推荐
        paper_res = session.query(papers.Papers).filter(papers.Papers.OPEN_ID == user_id).order_by(
                    papers.Papers.DATE_TIME.desc()).all()
        # 考研资讯
        post_res = session.query(postgraduate.Postgraduate).filter(
            postgraduate.Postgraduate.OPEN_ID == user_id).order_by(
            postgraduate.Postgraduate.DATE_TIME.desc()).all()

        # 提交即保存到数据库
        session.commit()
        ret = []
        ret.extend(parse_object(study_res))
        ret.extend(parse_object(play_res))
        ret.extend(parse_object(second_res))
        ret.extend(parse_object(found_res))
        ret.extend(parse_object(code_res))
        ret.extend(parse_object(contest_res))
        ret.extend(parse_object(paper_res))
        ret.extend(parse_object(post_res))

        # 计算每一页返回的数量
        page_start = page_index * config.PAGE_SIZE
        page_end = page_start + config.PAGE_SIZE

        # 再做一次按时间排序
        result = sorted(ret, key=lambda x: x['DATE_TIME'], reverse=True)[page_start:page_end]
        logging.info('OK : common.py--->get_latest_by_user() 成功')
        return result
    except Exception as e:
        session.rollback()
        logging.critical('Error : common.py--->get_latest_by_user()  失败 : {}'.format(e))
        return []
    finally:
        session.close()


def query_attention_by_user(**kwargs):
    """
    由 openid 查询其关于的 8 个表中的具体信息
    :param kwargs:  {'openid': openid}
    :return:
    """
    session = None
    try:
        user_id = kwargs['user_id']
        session = utils.get_session()
        obj_id = session.query(Attention.OBJECT_ID).filter(
                 Attention.OPEN_ID == user_id).order_by(Attention.DATE_TIME.desc()
                                                        ).limit(config.LIMIT_MAX).all()
        results = []
        for obj in obj_id:
            # 相约学习
            study_res = session.query(study.Study).filter(study.Study.OBJECT_ID == obj[0]).order_by(
                study.Study.DATE_TIME.desc()).all()
            # 约个球
            play_res = session.query(play.Play).filter(play.Play.OBJECT_ID == obj[0]).order_by(
                play.Play.DATE_TIME.desc()).all()
            # 二手闲置
            second_res = session.query(second_hand.SecondHand).filter(
                second_hand.SecondHand.OBJECT_ID == obj[0]).order_by(
                second_hand.SecondHand.DATE_TIME.desc()).all()
            # 失物招领
            found_res = session.query(found.Found).filter(found.Found.OBJECT_ID == obj[0]).order_by(
                found.Found.DATE_TIME.desc()).all()
            # 菜鸟编程
            code_res = session.query(coding.Code).filter(coding.Code.OBJECT_ID == obj[0]).order_by(
                coding.Code.DATE_TIME.desc()).all()
            # 竞赛
            contest_res = session.query(contest.Contest).filter(contest.Contest.OBJECT_ID == obj[0]).order_by(
                contest.Contest.DATE_TIME.desc()).all()
            # 论文推荐
            paper_res = session.query(papers.Papers).filter(
                papers.Papers.OBJECT_ID == obj[0]).order_by(
                papers.Papers.DATE_TIME.desc()).all()
            # 考研资讯
            post_res = session.query(postgraduate.Postgraduate).filter(
                postgraduate.Postgraduate.OBJECT_ID == obj[0]).order_by(
                postgraduate.Postgraduate.DATE_TIME.desc()).all()

            # 提交即保存到数据库
            session.commit()
            results.extend(parse_object(study_res))
            results.extend(parse_object(play_res))
            results.extend(parse_object(second_res))
            results.extend(parse_object(found_res))
            results.extend(parse_object(code_res))
            results.extend(parse_object(contest_res))
            results.extend(parse_object(paper_res))
            results.extend(parse_object(post_res))

        # session.commit()
        logging.info('OK : common.py--->query_msg_by_user()  成功 ')
        return results
    except Exception as e:
        session.rollback()
        logging.critical('Error : common.py--->query_msg_by_user()  失败 : {}'.format(e))
        return []
    finally:
        # 关闭session
        session.close()


if __name__ == '__main__':
    res = query_attention_by_user(**{'user_id': 'o7C2I5E-rhXE1Fpbru9fl_w_OM1U'})
    # o7C2I5E-rhXE1Fpbru9fl_w_OM1U  o7C2I5IZorGbj84FkojkGY7TqTeI
    # o7C2I5K-2wG1MbKaMNk0IsXg2U6g
