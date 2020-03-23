#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import struct


def change_chaddr_to_mac(chaddr):  # 转换16字节chaddr为MAC地址，前6字节为MAC，后面暂时无用！！
    mac_addr_int_list = struct.unpack('>16B', chaddr)[:6]
    mac_addr_list = []
    for mac_addr_int in mac_addr_int_list:
        if mac_addr_int < 16:
            mac_addr_list.append('0' + str(hex(mac_addr_int))[2:])
        else:
            mac_addr_list.append(str(hex(mac_addr_int))[2:])
    mac_addr = mac_addr_list[0] + ':' + mac_addr_list[1] + ':' + mac_addr_list[2] + ':' + mac_addr_list[3] + ':' + \
               mac_addr_list[4] + ':' + mac_addr_list[5]
    return mac_addr


if __name__ == '__main__':
    print(change_chaddr_to_mac(b'\x00PV\xabM\x19\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))
