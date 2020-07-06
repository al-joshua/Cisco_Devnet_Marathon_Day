from nornir import InitNornir
from nornir_scrapli.tasks import send_command
import sys


def get_host_data(task, command):
    """function gets and parses outputs from devices. Client - scrapli, parser - textfsm """

    try:
        result = task.run(task=send_command, command=command)
        structured_result = dict((k, v.scrapli_response.textfsm_parse_output()) for k, v in result.items())
    except Exception as err:
        print(f'Unable to pull data or parse it\n Reason is: {err}')
        sys.exit()

    return structured_result


def search_mac_address(task, mac):
    """search for mac address in collected data"""

    # pull 'show mac address-table' output and parse it via textfsm
    structured_mac_table = get_host_data(task, 'show mac address-table')

    # pull 'show interface status' output and parse it
    structured_interface_status = get_host_data(task, 'show interface status')

    # pull 'show interfaces' output and parse it
    structured_interfaces = get_host_data(task, 'show interfaces')

    for host in task.inventory.hosts.keys():
        for record in structured_mac_table[host]:
            if record['destination_address'] == mac:
                for interface in structured_interface_status[host]:
                    if interface['port'] == record['destination_port'] and interface['vlan'] != 'trunk':
                        return host, interface['port']

        for interface in structured_interfaces[host]:
            if interface['address'] == mac:
                return host, interface['interface']

    print(f'mac address {mac} was not found in the domain')
    sys.exit()


def main():
    """main function"""

    try:
        mac_address = sys.argv[1]
    except IndexError:
        print('Enter a mac address to search for in the following format - xxxx.yyyy.zzzz')
        sys.exit(1)

    nr = InitNornir(config_file='nornir_lab_config.yaml')
    switches = nr.filter(type='switch')
    switch, interface = search_mac_address(switches, mac_address)
    print(f'MAC Address {mac_address} is connected to switch {switch} interface {interface}')


if __name__ == '__main__':
    main()