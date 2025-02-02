import requests, json, os
from dotenv import load_dotenv

def get_template_id(session, name):
    url = f"{os.environ['VMANAGE_URL']}/dataservice/v1/config-group"
    headers = {
        "Content-Type" : 'application/json',
        "X-XSRF-TOKEN" : get_authentication_token(session)
    }
    config_groups = session.get(url, headers=headers, verify=False).json()
    for config_group in config_groups:
        if config_group['name'] == name:
            return config_group['id']

def get_device_id(session, name):
    url = f"{os.environ['VMANAGE_URL']}/dataservice/device"
    headers = {
        "Content-Type" : 'application/json',
        "X-XSRF-TOKEN" : get_authentication_token(session)
    }
    devices = session.get(url, headers=headers, verify=False).json()['data']
    for device in devices:
        if device['host-name'] == name:
            return device['uuid']

def get_authentication_token(session):
    url = f"{os.environ['VMANAGE_URL']}/dataservice/client/token"
    response = session.get(url, headers={'Content-Type': 'application/json'}, verify=False)
    return response.text

def get_authenticated_session():
    host = os.environ['VMANAGE_URL']
    username = os.environ['VMANAGE_USER']
    password = os.environ['VMANAGE_PASS']
    session = requests.session()
    url = f"{host}/j_security_check"
    headers = {
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = f"j_username={username}&j_password={password}"
    session.post(url, headers=headers, data=data, verify=False)
    return session

def associate_device(session, group, device):
    url = f"{os.environ['VMANAGE_URL']}/dataservice/v1/config-group/{group}/device/associate"
    headers = {
        "Content-Type" : 'application/json',
        "X-XSRF-TOKEN" : get_authentication_token(session)
    }
    body = {
        "devices": [
            {
                "id": device
            }
        ]
    }
    session.put(url, json=body, headers=headers, verify=False)

if __name__ == "__main__":
    load_dotenv()
    session = get_authenticated_session()

    group_id_1 = get_template_id(session, "aaa-packing-machine-1")
    group_id_2 = get_template_id(session, "aaa-packing-machine-2")
    device_id = get_device_id(session, os.environ['VMANAGE_DEVICE'])

    associate_device(session, group_id_1, device_id)
    # associate_device(session, group_id_2, device_id)