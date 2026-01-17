import zipfile
from io import BytesIO

import requests


def download_flags():
    """Download flag images from lipis/flag-icons"""
    url = "https://github.com/lipis/flag-icons/archive/main.zip"
    res = requests.get(url)
    with zipfile.ZipFile(BytesIO(res.content)) as zf:
        for entry in zf.infolist():
            if not entry.filename.endswith(".svg"):
                continue
            _, _, size, filename = entry.filename.split("/")
            if size != "4x3":
                continue
            with open("assets/images/flags/4x3/" + filename, "wb") as f:
                f.write(zf.read(entry))


def download_ipv4band():
    """Download ipv4 band list from KRNIC"""
    url = "https://한국인터넷정보센터.한국/jsp/statboard/IPAS/ovrse/natal/IPaddrBandCurrentDownload.jsp"
    res = requests.get(url)
    with open("assets/data/ipv4.csv", "wb") as f:
        f.write(res.content)


if __name__ == "__main__":
    download_flags()
    download_ipv4band()
