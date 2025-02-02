import requests, time, urllib3, os, json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

urllib3.disable_warnings()

load_dotenv()

device_ip = os.environ['DEVICE_IP']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

def turn_port_off():
    # GET operational status of port FastEthernet0/0/1
    url = f"https://{device_ip}/restconf/data/ietf-interfaces:interfaces/interface=FastEthernet0%2F0%2F1"
    response = requests.get(url,
                            auth=HTTPBasicAuth(username, password),
                            headers = {
                                "Accept" : "application/yang-data+json",
                                "Content-Type" : "application/yang-data+json"
                            }, verify=False).json()
    if response['ietf-interfaces:interface'][0]['enabled']:
        print("Interface FastEthernet0/0/1 is UP")
    else: 
        print("Interface FastEthernet0/0/1 is DOWN")

    # SET admin status to DOWN
    url = f"https://{device_ip}/restconf/data/ietf-interfaces:interfaces/interface=FastEthernet0%2F0%2F1"
    body = {
        "ietf-interfaces:interface":{
            "name":"FastEthernet0/0/1",
            "description":"Configured by RESTCONF",
            "type":"iana-if-type:ethernetCsmacd",
            "enabled": False
        }
    }
    response = requests.put(url,
                            auth=HTTPBasicAuth(username, password),
                            headers = {
                                "Accept" : "application/yang-data+json",
                                "Content-Type" : "application/yang-data+json"
                            }, data=json.dumps(body), verify=False)

    # GET operational status of port FastEthernet0/0/1
    url = f"https://{device_ip}/restconf/data/ietf-interfaces:interfaces/interface=FastEthernet0%2F0%2F1"
    response = requests.get(url,
                            auth=HTTPBasicAuth(username, password),
                            headers = {
                                "Accept" : "application/yang-data+json",
                                "Content-Type" : "application/yang-data+json"
                            }, verify=False).json()
    if response['ietf-interfaces:interface'][0]['enabled']:
        print("Interface FastEthernet0/0/1 is UP")
    else: 
        print("Interface FastEthernet0/0/1 is DOWN")

if __name__ == "__main__":
    turn_port_off()