#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import logging

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
import ipaddress
from multiprocessing.pool import ThreadPool
from net_1_arp.arp_request import arp_request


def scapy_arp_scan(network, ifname):
    net = ipaddress.ip_network(network)
    ip_list = []
    for ip_add in net:
        ip_list.append(str(ip_add))  # 把IP地址放入ip_list的清单
    pool = ThreadPool(processes=100)  # 创建多进程的进程池（并发为100）
    result = []
    for i in ip_list:
        result.append(pool.apply_async(arp_request, args=(i, ifname)))  # 关联函数与参数，并且添加结果到result
    pool.close()  # 关闭pool，不在加入新的进程
    pool.join()  # 等待每一个进程结束
    scan_dict = {}  # 扫描结果IP地址的清单
    # print(result)
    for r in result:
        if r.get()[1] is not None:  # 如果没有获得MAC，就continue进入下一次循环
            scan_dict[r.get()[0]] = r.get()[1]
    return scan_dict


if __name__ == '__main__':
    # Windows Linux均可使用
    import time

    t1 = time.time()
    print('活动IP地址如下:')
    for ip, mac in scapy_arp_scan("10.1.1.0/24", 'ens33').items():
        print('ip地址:'+ip+'是活动的,他的MAC地址是:'+mac)
    t2 = time.time()
    print('本次扫描时间: %.2f' % (t2 - t1))  # 计算并且打印扫描时间
