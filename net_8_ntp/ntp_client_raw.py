#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import socket
import struct
import datetime
time_1970 = 2208988800


def ntp_client(ntp_server):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket.AF_INET为IP，socket.SOCK_DGRAM为UDP
    data = b'\x1b' + 47 * b'\0'  # \x1b(00 011(版本3) 011(客户模式)) + 47个\0凑齐48个字节的头部
    client.sendto(data, (ntp_server, 123))  # 数据，IP地址和端口号
    data, address = client.recvfrom(1024)  # 接收缓存为1024
    if data:
        print('Response received from:', address)  # 如果收到数据，打印地址信息
    # s = struct.unpack('!12I', data)  # 48个字节，12个四字节
    # print (s)
    t = struct.unpack('!12I', data)[10]  # 倒数第二个为时间
    t -= time_1970  # Linux 自己的系統時間，由 1970/01/01 開始記錄的時間參數

    return datetime.datetime.fromtimestamp(t)


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    # # 试验台翻墙会影响代码执行
    print(ntp_client("0.uk.pool.ntp.org"))
