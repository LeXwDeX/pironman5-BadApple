
import requests
from utils import log
import os

def is_homeassistant_addon():
    return 'SUPERVISOR_TOKEN' in os.environ

def get(endpoint):
    try:
        url = f"{url}{endpoint}"
        r = requests.get(url, headers=headers)
        return r.json()
    except Exception as e:
        log(msg="home assistant get error: " + e, level='WARNING')

def set(endpoint, data=None):
    try:
        url = f"{url}{endpoint}"
        requests.post(url, headers=headers)
    except Exception as e:
        log(msg="home assistant get error: " + e, level='WARNING')

def get_ip():
    IPs = {}
    data = get("network/info")
    interfaces = data["data"]["interfaces"]
    for interface in interfaces:
        name = interface['interface']
        ip = interface['ipv4']['address']
        if len(ip) == 0:
            continue
        ip = ip[0]
        if ip == '':
            continue
        if "/" in ip:
            ip = ip.split("/")[0]
        IPs[name] = ip
    return IPs

def get_network_connection_type():
    connection_type_map = {
        "ethernet": "Wired",
        "wireless": "Wireless",
    }
    connection_type = []
    data = get("network/info")
    interfaces = data["data"]["interfaces"]
    for interface in interfaces:
        if interface['connected']:
            connection_type.append(connection_type_map[interface['type']])
    return connection_type

def shutdown():
    '''shutdown homeassistant host'''
    log.info(msg="Shutdown home assistant host")
    set("host/shutdown")


url="http://supervisor/"
token = None
if is_homeassistant_addon():
    token = os.environ['SUPERVISOR_TOKEN']
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}
