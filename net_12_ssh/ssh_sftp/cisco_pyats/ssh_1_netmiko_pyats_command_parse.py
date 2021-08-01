# pip3 install pyats_genie_command_parse
from pyats_genie_command_parse import GenieCommandParse
from net_12_ssh.ssh_sftp.ssh_client_netmiko import netmiko_show_cred
from pprint import pprint

# Linux环境
raw_result = netmiko_show_cred('10.1.1.253', 'admin', 'Cisc0123', 'show ip inter brie')
print(raw_result)

parse_obj = GenieCommandParse(nos='ios')
data = parse_obj.parse_string(show_command='show ip interface brief',
                              show_output_data=raw_result)
pprint(data)