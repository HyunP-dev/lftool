from functools import cache
from typing import TypedDict

import requests


class IPInfo(TypedDict):
    ip: str
    hostname: str
    city: str
    region: str
    country: str
    loc: str
    org: str
    postal: str
    timezone: str
    readme: str


@cache
def get_ip_info(ip):
    return IPInfo(**requests.get(f"https://ipinfo.io/{ip}/json").json())
