from snmpv2_getbulk import snmpv2_getbulk


def snmpv2_getall(ip, community, count=25, port=161):
    name_list = [x[1] for x in snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.2", count=count, port=port)]
    # print(name_list)

    speed_list = [x[1] for x in snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.5", count=count, port=port)]
    # print(speed_list)

    in_bytes_list = [x[1] for x in snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.10", count=count, port=port)]
    # print(in_bytes_list)

    out_bytes_list = [x[1] for x in snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.16", count=count, port=port)]
    # print(out_bytes_list)

    final_list = []
    for x in zip(name_list, speed_list, in_bytes_list, out_bytes_list):
        final_list.append({'name': x[0], 'speed': x[1], 'in_bytes': x[2], 'out_bytes': x[3]})

    return final_list


if __name__ == '__main__':
    from pprint import pprint

    final_list_result = snmpv2_getall("10.1.1.253", "tcpipro", count=25, port=161)

    pprint(final_list_result, indent=4)
