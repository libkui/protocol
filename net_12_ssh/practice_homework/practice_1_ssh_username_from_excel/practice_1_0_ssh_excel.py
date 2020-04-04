#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from net_12_ssh.practice_homework.practice_1_ssh_username_from_excel.practice_0_parser_excel_return_dict import excel_parser_return_dict
from net_12_ssh.practice_homework.practice_1_ssh_username_from_excel.practice_0_write_excel_openpyxl import excel_write
from net_12_ssh.ssh_sftp.ssh_client_multi_cmd import ssh_client_multi_cmd
from net_12_ssh.ssh_sftp.ssh_client_one_cmd import ssh_client_one_cmd
import re


def excel_user_to_ios(ip, username, password, excelfile):
    # 读取excel信息，返回字典！
    user_dict = excel_parser_return_dict(excelfile)
    # 产生配置命令
    cmds = ['configure terminal']
    for x, y in user_dict.items():
        cmd = 'username ' + x + ' privilege ' + str(y[1]) + ' password ' + str(y[0])
        cmds.append(cmd)
    # ssh登录路由器，配置用户信息
    ssh_client_multi_cmd(ip, username, password, cmds, verbose=False)


def excel_ios_user_to_excel(ip, username, password, excelfile):
    # 执行'sh run | in username'并提取结果
    show_run = ssh_client_one_cmd(ip, username, password, 'sh run | in username')
    # 把结果通过'\r\n'分离，产生清单
    show_run_list = show_run.split('\r\n')
    user_dict = {}
    for x in show_run_list:
        # 如果格式为username admin privilege 15 password 0 cisco，提取用户名，密码和级别
        if re.match(r'username (\w+) privilege (\d+) password \w (\w+)', x):
            re_result = re.match(r'username (\w+) privilege (\d+) password \w (\w+)', x).groups()
            user_dict[re_result[0]] = re_result[2], int(re_result[1])
        # 如果格式为username passuser password 0 12345，提取用户和密码，级别为1级
        elif re.match(r'username (\w+) password \w (\w+)', x):
            re_result = re.match(r'username (\w+) password \w (\w+)', x).groups()
            user_dict[re_result[0]] = re_result[1], 1
    # 把字典的用户名，密码和级别信息，写入Excel
    # sheel_name为IP地址
    excel_write(file=excelfile, sheel_name=ip, write_dict=user_dict)


if __name__ == '__main__':
    excel_user_to_ios('10.1.1.253', 'admin', 'Cisc0123', './excel_file/read_accounts.xlsx')
    excel_ios_user_to_excel('10.1.1.253', 'admin', 'Cisc0123', './excel_file/write_iosuser.xlsx')
