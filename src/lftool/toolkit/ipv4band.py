from __future__ import annotations

import ipaddress
from datetime import date
from functools import cache
from typing import NamedTuple, Optional

import polars as pl

ipv4_table = pl.read_csv("./assets/data/ipv4.csv", encoding="EUC-KR")
ipv4_table = ipv4_table.with_columns(
    ipv4_table["시작IP"]
    .map_elements(lambda ip: int(ipaddress.ip_address(ip)))
    .alias("start_ipv4")
)
ipv4_table = ipv4_table.with_columns(
    ipv4_table["끝IP"]
    .map_elements(lambda ip: int(ipaddress.ip_address(ip)))
    .alias("end_ipv4")
)


class IPv4RBand(NamedTuple):
    country: str
    start: ipaddress.IPv4Address
    end: ipaddress.IPv4Address
    prefix: str
    date: date

    @cache
    @staticmethod
    def of(ipaddr: str) -> Optional[IPv4RBand]:
        ip = ipaddress.ip_address(ipaddr)
        condition = (pl.col("start_ipv4") <= int(ip)) & (int(ip) <= pl.col("end_ipv4"))
        if ip.is_global:
            _, *data, _, _ = ipv4_table.filter(condition).row(0)
            return IPv4RBand(*data[:-1], date.fromisoformat(str(data[-1])))
        return None
