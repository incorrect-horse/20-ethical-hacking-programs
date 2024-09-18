import requests


def download(url):
    get_response = requests.get(url, verify=False)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as output:
        output.write(get_response.content)
    return


URL = "https://i.natgeofe.com/n/5f35194b-af37-4f45-a14d-60925b280986/NationalGeographic_2731043_2x3.jpg"
download(URL)

print("Goodbye!")
