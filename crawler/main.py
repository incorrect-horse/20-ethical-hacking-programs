import requests


def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


def discover_subdomains(tgt_url):
    word_list = "./files/subdomains-wordlist.txt"
    with open(word_list, "r") as wordlist:
        for line in wordlist:
            word = line.strip()
            test_url = word + "." + tgt_url
            response = request(test_url)
            if response:
                print(f"[+] Discovered subdomain --> {test_url}")
    return


def discover_files_and_directories(tgt_url):
    word_list = "./files/files-and-dirs-wordlist.txt"
    with open(word_list, "r") as wordlist:
        for line in wordlist:
            word = line.strip()
            test_url = tgt_url + "/" + word
            response = request(test_url)
            if response:
                print(f"[+] Discovered URL --> {test_url}")
    return


# target_url = "google.com"
target_url = "10.0.2.6/mutillidae/"

try:
    # discover_subdomains(target_url)
    discover_files_and_directories(target_url)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... terminating app, please wait.")

print("Goodbye!")
