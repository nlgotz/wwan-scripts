#!/usr/bin/env python

import os, sys

if __name__ == '__main__':
    if sys.argv[1] == "start":
        os.system("qmicli -d /dev/cdc-wdm0 --device-open-mbim --dms-set-fcc-authentication")
        os.system("mbim-network /dev/cdc-wdm0 start")
        interface = os.popen('qmicli -d /dev/cdc-wdm0 -p -w').read().strip()
        get_settings = os.popen('qmicli -d /dev/cdc-wdm0 -p --wds-get-current-settings').read()
        for item in get_settings.split('\n'):
            if 'IPv4 address: ' in item:
                ip_address = item.split(': ')[1]
            if 'IPv4 gateway address' in item:
                gateway = item.split(': ')[1]
            if 'MTU' in item:
                mtu = item.split(': ')[1]
        # Set Interfaces
        print "IP address: {}".format(ip_address)
        print "Gateway:    {}".format(gateway)
        print "MTU:        {}".format(mtu)
        os.system("ip addr add {}/30 dev {}".format(ip_address, interface))
        os.system("ip link set dev {} mtu {}".format(interface, mtu))
        os.system("ip link set dev {} up".format(interface))
        os.system("ip route add default via {} dev {} metric 1000".format(gateway, interface))
    elif sys.argv[1] == "stop":
        interface = os.popen('qmicli -d /dev/cdc-wdm0 -p -w').read().strip()
        os.system("mbim-network /dev/cdc-wdm0 stop")
        os.system("ip link set dev {} down".format(interface))
        os.system("ip addr flush dev {}".format(interface))
    else:
        print "Please run this command as root with either start or stop"
