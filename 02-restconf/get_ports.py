import requests, time, urllib3, os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

urllib3.disable_warnings()

load_dotenv()

device_ip = os.environ['DEVICE_IP']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

def get_ports():
    # Craft RESTCONF request for getting port status
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
    print('------------------')

if __name__ == "__main__":
    # Infinite loop executing RESTCONF GET requests
    while True:
        get_ports()
        time.sleep(2)