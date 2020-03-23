import logging

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import in6_getnsma, inet_pton
import socket
import ipaddr


def solicited_node_multicast_address(ipv6_address):
    ipv6_b = in6_getnsma(inet_pton(socket.AF_INET6, ipv6_address))
    return ipaddr.IPv6Address(ipaddr.Bytes(ipv6_b)).__str__()


if __name__ == '__main__':
    print(solicited_node_multicast_address('2001::f107:94ac:2717:a736'))


