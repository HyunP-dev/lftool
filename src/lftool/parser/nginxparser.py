from typing import NamedTuple


class NGINXAccessLog(NamedTuple):
    remote_addr: str
    remote_user: str
    time_local: str
    request: str
    status: int
    body_bytes_sent: int
    http_referer: str
    http_user_agent: str
    http_x_forwarded_for: str


def parse_access_log(line: str) -> NGINXAccessLog:
    remote_addr, remains = line.split(" - ", 1)
    remote_user, remains = remains.split(" [", 1)
    time_local, remains = remains.split('] "', 1)
    request, remains = remains.split('" ', 1)
    status, remains = remains.split(" ", 1)
    body_bytes_sent, remains = remains.split(' "', 1)
    http_referer, remains = remains.split('" "', 1)
    if len(tokens := remains.split('" "', 1)) > 1:
        http_user_agent, remains = tokens
    else:
        http_user_agent = tokens[0].split('"')[0]
        remains = ""
    if remains:
        http_x_forwarded_for, _ = remains.split('"', 1)
    else:
        http_x_forwarded_for = None
    return NGINXAccessLog(
        remote_addr=remote_addr,
        remote_user=remote_user,
        time_local=time_local,
        request=request,
        status=int(status),
        body_bytes_sent=int(body_bytes_sent),
        http_referer=http_referer,
        http_user_agent=http_user_agent,
        http_x_forwarded_for=http_x_forwarded_for,
    )
