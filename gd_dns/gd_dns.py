#!/usr/bin/python

import requests, json
import gd_dns_config as config

godaddy_headers = {"Authorization":" sso-key " + config.godaddy_key + ":" + config.godaddy_secret}

def get_current_record(domain: str, record_name: str, record_type: str = "A") -> [str, bool]:
    """Attempts to find the current data for a DNS record, returns the data or error code and bool indicating success"""
    req = requests.get(config.godaddy_apiurl 
                        + domain + "/records/" + record_type + "/" + record_name,
                        headers=godaddy_headers)
    js = json.loads(req.text)
    if req.status_code == 200:
        if len(req.text) > 3:
            return js[0]["data"], True
        else:
            return config.record_name + "." + config.godaddy_domain + " not found", False
    return js["code"], False


def get_currentip() -> str:
    """Returns the current apparent external IP of the host running this"""
    req = requests.get("http://ipinfo.io/json")
    ip = req.json()["ip"]
    return ip


def set_record(domain: str, record_name: str, record_type: str, data: str) -> bool:
    """Sets the data for a record given the domain and record name and type, returns a bool indicating success"""
    content = [{"data": data, "name": record_name, "ttl": 36000, "type": record_type}]
    req = requests.put(config.godaddy_apiurl 
                        + domain + "/records/" + record_type + "/" + record_name,
                        headers=godaddy_headers, json=content )
    if req.status_code == 200:
        return True
    return False


wan_ip = get_currentip()
current_dns = get_current_record(config.godaddy_domain, config.record_name, "A")

if current_dns[1] == False:
    print("An error occured:", current_dns[0])
    exit(1)

if wan_ip != current_dns[0]:
    print("DNS record is out of date ( WAN =", wan_ip, ", DNS =", current_dns[0], ")")
    print("Updating record: " + config.record_name + "." + config.godaddy_domain)
    if(set_record(config.godaddy_domain, config.record_name, "A", wan_ip)):
        print("Updated successfully")
        exit(0)
    else:
        print("Failed to update")
        exit(1)
else:
    print("All up to date")
