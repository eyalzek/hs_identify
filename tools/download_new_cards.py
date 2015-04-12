import requests


def download_file(card):
    r = requests.get(card["url"], stream=True)
    r.raise_for_status()
    filename = card["name"].replace(":", "#") + ".png"
    with open(filename, "w+") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
