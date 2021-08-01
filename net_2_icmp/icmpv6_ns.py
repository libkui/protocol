#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

# IPv6参考文档
# https://www.idsv6.de/Downloads/IPv6PacketCreationWithScapy.pdf
# https://www.ernw.de/download/Advanced%20Attack%20Techniques%20against%20IPv6%20Networks-final.pdf

import logging

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import *
from tools.get_mac_netifaces import get_mac_address
from tools.ipv6_tools import mac_to_ipv6_linklocal
from tools.ipv6_tools_kamene import solicited_node_multicast_address

# Windows 查看IPv6邻居 netsh int ipv6 show neigh
# IOS     查看IPv6邻居 show ipv6 neighbors
# Linux   查看IPv6邻居 ip -6 neigh                 | ping6 2001:1::200


def icmpv6_ns(host, ifname):  # 请求特定IPv6地址的MAC地址
    ll_mac = get_mac_address(ifname)  # 获取本机接口MAC地址
    # 构建icmpv6_ns数据包

    # -----------IPv6头部 - -----------
    # Next Header: 0x3A(ICMPv6)
    # 原地址: Link Local address
    # 目的地址: Solicited node multicast address # 请求节点组播地址
    #
    # ----------ICMPv6头部 - ---------
    # ICMPv6 Type: 135
    # ICMPv6 Code: 0(NS)
    # 目标地址: 2001:1::253
    #
    # ----Source Link-Layer Address - ---
    # 源地址: 00:50:56:AB:25:08(本地MAC地址)

    # 所有可选都填写
    # packet = IPv6(src=mac_to_ipv6_linklocal(ll_mac),
    #               dst=solicited_node_multicast_address(host)) / ICMPv6ND_NS(tgt=host) / ICMPv6NDOptSrcLLAddr(lladdr=ll_mac)

    # 下面是最精简
    # 系统自动产生, IPv6头部(linklocal地址, 请求节点组播地址(并且转换到组播MAC))
    # 没有ICMPv6NDOptSrcLLAddr头部一样正常工作
    packet = IPv6() / ICMPv6ND_NS(tgt=host)
    # packet.show()

    # 发送数据包
    result = sr1(packet, timeout=2, verbose=False)

    # 提取返回的MAC地址
    # result.show()
    return result.getlayer("ICMPv6 Neighbor Discovery Option - Destination Link-Layer Address").fields['lladdr']


if __name__ == '__main__':
    # Windows Linux均可使用
    print(icmpv6_ns("2001:1::253", 'ens160'))
