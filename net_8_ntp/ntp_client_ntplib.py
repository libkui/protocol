#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import ntplib
from time import ctime
import datetime


def ntp_client(ntp_server):
    c = ntplib.NTPClient()
    response = c.request(ntp_server, version=3)
    # print(response.tx_time) # 1596243472.7740922 为timestamp
    return datetime.datetime.fromtimestamp(response.tx_time)


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    print(ntp_client('0.cn.pool.ntp.org'))
