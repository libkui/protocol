from netmiko import Netmiko


def netmiko_show_cred(host, username, password, cmd, enable='Cisc0123', ssh=True):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': 'cisco_ios' if ssh else 'cisco_ios_telnet',
                    'secret': enable
    }
    try:
        net_connect = Netmiko(**device_info)
        return net_connect.send_command(cmd)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


if __name__ == '__main__':
    raw_result = netmiko_show_cred('10.1.1.253', 'admin', 'Cisc0123', 'show run')
    print(type(raw_result))
    print(raw_result)
