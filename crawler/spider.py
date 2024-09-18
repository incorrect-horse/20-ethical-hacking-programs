import requests
import re
from urllib.parse import urljoin


def extract_links(url):
    response = requests.get(url)
    return re.findall(r'(?:href=")(.*?)"', response.content.decode(errors="ignore"))


def crawl(url):
    href_links = extract_links(url)

    for link in href_links:
        link = urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)
    return target_links


target_url = "http://10.0.2.6/mutillidae/"
target_links = []

try:
    crawl(target_url)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... terminating app, please wait.")

print("Goodbye!")
