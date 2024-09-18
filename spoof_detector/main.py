# testphp.vulnweb.com/login.php
import scapy.all as scapy


def get_mac(ip_address):
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, verbose=False, timeout=1)[0]
    return answered_list[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    return


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].psrc
            if real_mac != response_mac:
                print("[+] Pew! Pew! You're under attack!!")
            #print(packet.show())
        except IndexError:
            pass
    return


sniff("enp0s3")

print("\nGoodbye!")
