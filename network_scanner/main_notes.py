# Dependencies:
# sudo apt install netdiscover
# sudo apt install scapy

# import scapy.all as scapy
# def scan(ip_address):
#     scapy.arping(ip_address)
#     return
# scan("10.0.2.2/24")

import scapy.all as scapy


def old_scan(ip_address):
    arp_request = scapy.ARP(pdst=ip_address)
    #print(arp_request) # returns binary string
    #scapy.ls(scapy.ARP()) # use 'ls' to display field options for 'ARP'
    #print(arp_request.summary())
    #arp_request.show()
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #scapy.ls(scapy.Ether()) # 'Ether' class options
    #print(broadcast.summary())
    #broadcast.show()
    arp_request_broadcast = broadcast/arp_request
    #print(arp_request_broadcast.summary())
    #arp_request_broadcast.show()
    #answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1)
    answered_list = scapy.srp(arp_request_broadcast, verbose=False, timeout=1)[0]
    #print(answered_list.summary())
    #print(unanswered_list.summary()) # show unused IP addresses
    print("\nIP Address\t\tMAC Address\n# # # # # # # # # # # # # # # # # # # # # #")
    for i in answered_list:
        #print(i[1].show())
        print(f"{i[1].psrc}\t\t{i[1].hwsrc}")
        #print("# # # # # # # # # # #")
    return


def scan(ip_address):
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, verbose=False, timeout=1)[0]

    #print("\nIP Address\t\tMAC Address\n# # # # # # # # # # # # # # # # # # # # # #")
    clients_list = []
    for i in answered_list:
        client_dict = {"ip": i[1].psrc, "mac": i[1].hwsrc}
        clients_list.append(client_dict)
        #print(f"{i[1].psrc}\t\t{i[1].hwsrc}")
    #print(clients_list)
    #return
    return clients_list


def print_scan_results(results_list):
    print("\nIP Address\t\tMAC Address\n# # # # # # # # # # # # # # # # # # # # # #")
    for client in results_list:
        print(f"{client['ip']}\t\t{client['mac']}")
    return


#target_client = {"mac": "", "ip": "", "os": ""}

# #scan("10.0.2.2/24")
# scan_result = scan("10.0.2.2/24")
# print_scan_results(scan_result)

print_scan_results(scan("10.0.2.2/24"))
