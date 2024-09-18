import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass


URL = "http://10.0.2.6/mutillidae/index.php?page=dns-lookup.php"
response = request(URL)
parsed_html = bs(response.content, "html.parser")
forms_list = parsed_html.findAll("form")

for form in forms_list:
    action = form.get("action")
    post_url = urljoin(URL, action)
    method = form.get("method")

    inputs_list = form.findAll("input")
    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = "test"
        post_data[input_name] = input_value
    result = requests.post(post_url, data=post_data)
    print(result.content.decode())

try:
    pass
except KeyboardInterrupt:
    print("\n[-] Detected CTRL+C ... terminating app, please wait.")

print("Goodbye!")
