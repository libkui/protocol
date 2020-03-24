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
from tools.get_mac_netifaces import get_mac_address
from tools.change_mac_to_bytes import change_mac_to_bytes
from tools.scapy_iface import scapy_iface  # 获取scapy iface的名字
import time
import struct
# Dynamic Host Configuration Protocol (DHCP) and Bootstrap Protocol (BOOTP) Parameters
# https://www.iana.org/assignments/bootp-dhcp-parameters/bootp-dhcp-parameters.xhtml
requested_option_1 = 1   # Subnet Mask
requested_option_2 = 6   # Domain Name Servers
requested_option_3 = 15  # Domain Name
requested_option_4 = 44  # NetBIOS (TCP/IP) Name Servers
requested_option_5 = 3   # Routers
requested_option_6 = 33  # Static Routes
requested_option_7 = 150  # TFTP Server address
requested_option_8 = 43  # Vendor Specific Information

bytes_requested_options = struct.pack("8B",
                                      requested_option_1,
                                      requested_option_2,
                                      requested_option_3,
                                      requested_option_4,
                                      requested_option_5,
                                      requested_option_6,
                                      requested_option_8,
                                      requested_option_7)


def chaddr(info):
    # chaddr一共16个字节，正常的chaddr信息里边只有MAC地址,思科比较特殊
    # MAC地址只有6个字节，所以需要把剩余部分填充b'\x00'
    return info + b'\x00' * (16 - len(info))


def dhcp_discover_sendonly(ifname, mac_address, wait_time=1):
    bytes_mac = change_mac_to_bytes(mac_address)  # 把MAC地址转换为二进制格式
    # param_req_list为请求的参数，没有这个部分服务器只会回送IP地址，什么参数都不给
    discover = Ether(dst='ff:ff:ff:ff:ff:ff',
                     src=mac_address,
                     type=0x0800) / IP(src='0.0.0.0',
                                       dst='255.255.255.255') \
                                  / UDP(dport=67,
                                        sport=68) \
                                  / BOOTP(op=1,
                                          chaddr=chaddr(bytes_mac)) \
                                  / DHCP(options=[('message-type', 'discover'),
                                                  ('param_req_list', bytes_requested_options),
                                                  'end'])

    if wait_time != 0:
        time.sleep(wait_time)
        sendp(discover,
              iface=scapy_iface(ifname),
              verbose=False)
    else:
        sendp(discover,
              iface=scapy_iface(ifname),
              verbose=False)


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    local_mac = get_mac_address('Net1')
    dhcp_discover_sendonly('Net1', local_mac)
