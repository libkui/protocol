#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import logging

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import *
from tools.get_ip_netifaces import get_ip_address  # 获取本机IP地址
from tools.get_mac_netifaces import get_mac_address  # 获取本机MAC地址
from tools.scapy_iface import scapy_iface  # 获取scapy iface的名字
from tools.get_ifname import get_ifname  # 获取接口唯一ID


def arp_request(ip_address):
    # 获取本机IP地址
    # localip = get_ip_address(ifname)
    # 获取本机MAC地址
    # localmac = get_mac_address(ifname)
    try:  # 发送ARP请求并等待响应
        result_raw = sr1(ARP(
                             # 注释掉的都为可选项
                             # op=1,
                             # hwsrc=localmac,
                             # hwdst='00:00:00:00:00:00',
                             # psrc=localip,
                             pdst=ip_address),
                         timeout=1,
                         verbose=False)
        return ip_address, result_raw.getlayer(ARP).fields.get('hwsrc')

    except AttributeError:
        return ip_address, None


if __name__ == "__main__":
    # Windows Linux均可使用
    arp_result = arp_request('10.1.1.101')
    print("IP地址:", arp_result[0], "MAC地址:", arp_result[1])
