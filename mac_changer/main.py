import subprocess as sp
import optparse
import re

# int: enp0s3
# mac: 08:00:27:ab:ca:11


def check_valid_mac(input):
    mac_format = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    if re.search(mac_format, input):
        return True
    else:
        return False

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Set interface to change MAC address")
    parser.add_option("-m", "--mac", dest="mac_address", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if check_valid_mac(options.mac_address) == False:
        print("[-] MAC address not valid, check input and try again.")
        #exit()
    if not len(options.mac_address) == 17:
        parser.error("[-] MAC address entered is not valid, use --help for more info.")
    if not options.interface:
        parser.error("[-] Please enter an interface, use --help for more info.")
    elif not options.mac_address:
        parser.error("[-] Please enter a MAC address, use --help for more info.")
    return options


def get_mac_address(interface):
    ifconfig_result = sp.check_output(["ifconfig", interface])
    ifconfig_result = ifconfig_result.decode('utf-8')
    mac_address_search_result = re.search(r"[0-9a-f][0-9a-f]:[0-9a-f][0-9a-f]:[0-9a-f][0-9a-f]:[0-9a-f][0-9a-f]:[0-9a-f][0-9a-f]:[0-9a-f][0-9a-f]", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")
    return


def change_mac_address(interface, mac_address):
    print(f"[+] Shutting down interface: {interface}")
    sp.call(["sudo", "ifconfig", interface, "down"])

    print(f"[+] Changing MAC address for {interface} to {mac_address}")
    sp.call(["sudo", "ifconfig", interface, "hw", "ether", mac_address])

    print(f"[+] Starting interface: {interface}")
    sp.call(["sudo", "ifconfig", interface, "up"])

    #print(f"\nIFCONFIG: {interface}")
    #sp.call(["ifconfig", interface])
    return

options = get_arguments()
current_mac = get_mac_address(options.interface)
print(f"[+] Current MAC address on interface '{options.interface}': {current_mac}.")

change_mac_address(options.interface, options.mac_address)

current_mac = get_mac_address(options.interface)
if current_mac == options.mac_address:
    print(f"[+] MAC address on interface '{options.interface}' was successfully changed to {current_mac}.")
else:
    print("[-] MAC address was not changed.")
