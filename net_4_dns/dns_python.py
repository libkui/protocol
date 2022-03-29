#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import dns.resolver


def dnspython(domain, q_type="A"):
    result = dns.resolver.resolve(domain, q_type)
    return_result = []
    if q_type == "A" or q_type == "AAAA":
        # print(result.response.answer)
        for i in result.response.answer:
            # print(i.items)
            for j in i.items:
                return_result.append(j.address)
    elif q_type == "CNAME" or q_type == "NS":
        for i in result.response.answer:
            for j in i.items:
                return_result.append(j.to_text())
    elif q_type == 'MX':
        for i in result:
            return_result.append({'MX preference': i.preference, 'mail exchanger': i.exchange.to_text()})
    return return_result


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    print(dnspython("cisco.com", q_type="A"))
    print(dnspython("www.cisco.com", q_type="CNAME"))
    print(dnspython("cisco.com", q_type="NS"))
    print(dnspython("cisco.com", q_type="MX"))
