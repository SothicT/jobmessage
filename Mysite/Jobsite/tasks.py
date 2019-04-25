#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from celery import task
from Spider.JobSpiderByZL import GetJobMessagebyzl
from Spider.JobSpiderBy51job import GetJobMessageby51


@task()
def add(x, y):
    return x + y


@task()
def run_test_suit(ts_id):
    print('++++++++++++++++++++++++++++++')
    print('jobs[ts_id=%s] running....' % ts_id)
    time.sleep(10.0)
    print('jobs[ts_id=%s] done' % ts_id)
    result = True
    return result

@task()
def spider_jobmessage(select, spidertext, spider_num):
    num = int(spider_num) + 1
    if select == 'ZLJOB':
        print('正在爬取来自'+select+'关于'+spidertext+'的数据。。。')
        spider = GetJobMessagebyzl(spidertext, 1, num, 'jobsite_jobmessagebyzl')
        print('爬取完成'+select)
    elif select == '51JOB':
        print('正在爬取来自' + select + '关于' + spidertext + '的数据。。。')
        spider = GetJobMessageby51(spidertext, 1, num, 'jobsite_jobmessageby51')
        print('爬取完成'+select)
    result = True
    return result


