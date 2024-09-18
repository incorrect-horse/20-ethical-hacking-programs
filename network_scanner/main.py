import scapy.all as scapy
import optparse
import re


def check_valid_ip(input):
    ip_format = r"(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}(?:/\b([0-9]|[11][0-9]|2[0-4])\b)?"
    if re.search(ip_format, input):
        return True
    else:
        return False


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Set IP address range to scan")
    (options, arguments) = parser.parse_args()
    if not options.target:
        #parser.error("[-] Please enter an IP address, use --help for more info.")
        print("[-] Arguments not given, proceeding manually.")
        options.target = input("[+] Enter a target IP range to scan: ")
    if check_valid_ip(options.target) == False:
        print("[-] IP address not valid, check input and try again.")
        exit()
    return options


def scan(ip_address):
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, verbose=False, timeout=1)[0]

    clients_list = []
    for i in answered_list:
        client_dict = {"ip": i[1].psrc, "mac": i[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list


def print_scan_results(results_list):
    print("\nIP Address\t\tMAC Address\n# # # # # # # # # # # # # # # # # # # # # #")
    for client in results_list:
        print(f"{client['ip']}\t\t{client['mac']}")
    return


# options = get_arguments()
# scan_results = scan(options.target)
# print_scan_results(scan_results) # 10.0.2.2/24

# options = get_arguments()
# print_scan_results(scan(options.target)) # 10.0.2.2/24

try:
    print_scan_results(scan(get_arguments().target)) # 10.0.2.2/24
except AttributeError:
    #pass
    print("\n[-] Hmm... Attribute error--something's missing")
except PermissionError:
    print("\n[-] Oops! Permission error--got root?")
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... Resetting ARP tables, please wait.")

print("\nGoodbye!")
