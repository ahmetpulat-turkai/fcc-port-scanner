import re
import socket
from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    is_ip = re.fullmatch(r"[\d.]+", target) is not None
    try:
        ip = socket.gethostbyname(target)
    except (socket.gaierror, UnicodeError):
        return "Error: Invalid IP address" if is_ip else "Error: Invalid hostname"

    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
        except OSError:
            pass
        finally:
            s.close()

    if not verbose:
        return open_ports

    host = None
    if is_ip:
        try:
            host = socket.gethostbyaddr(ip)[0]
        except OSError:
            host = None
    else:
        host = target
    header = f"Open ports for {host} ({ip})" if host else f"Open ports for {ip}"
    lines = [header, "PORT     SERVICE"]
    for port in open_ports:
        lines.append(f"{str(port).ljust(9)}{ports_and_services.get(port, '')}")
    return "\n".join(lines)
