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
import time
from net_6_dhcp.dhcp_discover import chaddr
from tools.scapy_iface import scapy_iface  # 获取scapy iface的名字

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


def dhcp_request_sendonly(ifname, dhcp_options, param_req_list, wait_time=1):
    request = Ether(dst='ff:ff:ff:ff:ff:ff',
                    src=dhcp_options['MAC'],
                    type=0x0800) / IP(src='0.0.0.0',
                                      dst='255.255.255.255') \
                                 / UDP(dport=67, sport=68) \
                                 / BOOTP(op=1,
                                         chaddr=chaddr(dhcp_options['client_id']),
                                         siaddr=dhcp_options['Server_IP'], ) \
                                 / DHCP(options=[('message-type', 'request'),
                                                 ('server_id', dhcp_options['Server_IP']),
                                                 ('requested_addr', dhcp_options['requested_addr']),
                                                 # Hardware_Type = 1(一个字节),需要添加在client_id前面
                                                 ('client_id', b'\x01' + dhcp_options['client_id']),
                                                 ('param_req_list', param_req_list),
                                                 'end'])
    if wait_time != 0:
        time.sleep(wait_time)
        sendp(request,
              iface=scapy_iface(ifname),
              verbose=False)
    else:
        sendp(request,
              iface=scapy_iface(ifname),
              verbose=False)


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    options = {'MAC': '00:0c:29:8d:5c:b6', 'Server_IP': '10.1.1.200', 'requested_addr': '10.1.1.235',
               'client_id': b'\x00\x0c)\x8d\\\xb6'}
    dhcp_request_sendonly('Net1', options, bytes_requested_options)
