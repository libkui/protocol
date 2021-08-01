from snmpv2_getbulk import snmpv2_getbulk


def get_if_oid(ip, community, if_name):
    if_result = snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.2", count=25, port=161)

    if_result_dict = {}
    for x, y in if_result:
        if_result_dict.update({y: x})

    if_oid = if_result_dict.get(if_name)
    if_oid_final = if_oid.replace('SNMPv2-SMI::mib-2.2.2.1.2', '1.3.6.1.2.1.2.2.1.7')
    return if_oid_final


if __name__ == '__main__':
    no_shutdown_oid = get_if_oid('10.1.1.253', 'tcpipro', 'GigabitEthernet2')
    print(no_shutdown_oid)
    from snmpv2_set import snmpv2_set
    snmpv2_set("10.1.1.253", "tcpiprw", no_shutdown_oid, 1, port=161)
