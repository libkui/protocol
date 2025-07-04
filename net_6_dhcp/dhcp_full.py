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

from multiprocessing.pool import ThreadPool
from tools.change_mac_to_bytes import change_mac_to_bytes
from tools.get_mac_netifaces import get_mac_address
from tools.change_chaddr_to_mac import change_chaddr_to_mac
from tools.scapy_iface import scapy_iface  # 获取scapy iface的名字
from net_6_dhcp.dhcp_discover import dhcp_discover_sendonly
from net_6_dhcp.dhcp_request import dhcp_request_sendonly

pool = ThreadPool(processes=10)


def dhcp_monitor_control(pkt):
    print(pkt.getlayer(DHCP).fields)
    print(pkt.getlayer(BOOTP).fields)
    try:
        if pkt.getlayer(DHCP).fields['options'][0][1] == 1:  # 发现并且打印DHCP Discover
            print('------发现DHCP Discover包，MAC地址为:', end='')
            mac_bytes = pkt.getlayer(BOOTP).fields['chaddr']  # 提取Discover中的Client Hardware Addr
            print(len(mac_bytes))

            mac_addr = change_chaddr_to_mac(mac_bytes)  # 把Client Hardware Addr转换为MAC地址
            print(mac_addr)  # 打印MAC地址
            print('Request包中发现如下Options:')
            # 如下For循环,提取DHCP的选项信息,并且打印,param_req_list没有做解码字节打印
            print(pkt.getlayer(DHCP).fields['options'])
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == 'end':
                    continue
                elif str(option[0]) == 'param_req_list':  # 记录请求参数清单
                    global param_req_list
                    param_req_list = option[1]
                # 打印所有选项
                print('%-15s ==> %s' % (str(option[0]), str(option[1])))

        elif pkt.getlayer(DHCP).fields['options'][0][1] == 2:  # 发现并且打印DHCP OFFER
            options = {}
            # 提取OFFER中的Client Hardware Addr
            mac_bytes = pkt.getlayer(BOOTP).fields['chaddr']
            # 把Client Hardware Addr转换为MAC地址
            mac_addr = change_chaddr_to_mac(mac_bytes)
            # 把从OFFER得到的信息读取并且写入options字典
            options['MAC'] = mac_addr
            options['client_id'] = change_mac_to_bytes(mac_addr)
            options['requested_addr'] = pkt.getlayer(BOOTP).fields['yiaddr']
            print('------发现DHCP OFFER包，请求者得到的IP为:' + pkt.getlayer(BOOTP).fields['yiaddr'])
            print('OFFER包中发现如下Options:')
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == 'end':
                    break
                # 提取server_id选项,写入options字典
                elif option[0] == 'server_id':
                    options['Server_IP'] = option[1]
                # 打印所有选项
                print('%-15s ==> %s' % (str(option[0]), str(option[1])))
            # 发送DHCP Request,把从OFFER提取的选项和param_req_list信息,发送给制造DHCP Request的函数
            pool.apply_async(dhcp_request_sendonly, args=(global_if, options, param_req_list))

        elif pkt.getlayer(DHCP).fields['options'][0][1] == 3:  # 发现并且打印DHCP Request
            print('------发现DHCP Request包，请求的IP为:' + pkt.getlayer(BOOTP).fields['yiaddr'])
            print('Request包中发现如下Options:')
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == 'end':
                    break
                elif str(option[0]) == "client_id":
                    # 在打印client_id时,转换为MAC地址,便于客户查看
                    print('%-15s ==> %s' % (str(option[0]), str(option[1])
                                            + " 转换为MAC:" + change_chaddr_to_mac(option[1][1:] + b"\x00" * (16 - len(option[1][1:])))
                                            )
                         )
                else:
                    # 打印其它所有选项,param_req_list保持原始字节形式打印
                    print('%-15s ==> %s' % (str(option[0]), str(option[1])))
        elif pkt.getlayer(DHCP).fields['options'][0][1] == 5:  # 发现并且打印DHCP ACK
            print('----发现DHCP ACK包，确认的IP为:' + pkt.getlayer(BOOTP).fields['yiaddr'])
            print('ACK包中发现如下Options:')
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == 'end':
                    break
                # 打印DHCP ACK的所有选项
                print('%-15s ==> %s' % (str(option[0]), str(option[1])))
    except Exception as e:
        print(e)
        pass


def dhcp_full(ifname, mac_address, timeout=3):
    global global_if
    global_if = ifname
    # 发送DHCP Discover数据包
    pool.apply_async(dhcp_discover_sendonly, args=(global_if, mac_address))
    # 侦听数据包,使用过滤器filter="port 68 and port 67"进行过滤,把捕获的数据包发送给DHCP_Monitor_Control函数进行处理
    sniff(prn=dhcp_monitor_control,
          filter="port 68 and port 67",
          store=0,
          iface=scapy_iface(global_if),
          timeout=timeout)


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    dhcp_full('Net1', get_mac_address('Net1'))
