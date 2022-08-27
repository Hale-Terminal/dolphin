import requests
import psutil

from dolphin import config


headers = {"accept": "application/json"}


def get_cpu():
    cpu_usage = psutil.cpu_percent(interval=1)
    return cpu_usage


def get_ram():
    ram_usage = psutil.virtual_memory().percent
    return ram_usage


def check_status(ip_address):
    try:
        r = requests.get(f"http://{ip_address}/api/v1/healthcheck")
        if r.status_code == 200:
            status = "UP"
        else:
            status = "DOWN"
    except Exception:
        status = "DOWN"
    return status


def get_ip():
    ip_address = requests.get("https://api.ipify.org").content.decode("utf8")
    return ip_address


def register(data, app):
    r = requests.post(
        f"http://{config.COSMOS_SERVER}/cosmos/v1/apps/{app}", headers=headers, json=data
    )
    print("Register")
    print(r.status_code)


def update(data, app, instance):
    r = requests.put(
        f"http://{config.COSMOS_SERVER}/cosmos/v1/apps/{app}/{instance}", headers=headers, json=data
    )
    print("Update")
    print(r.status_code)


def run():
    app = config.APP_NAME
    ip_address = get_ip()
    status = check_status(ip_address)
    port = config.PORT
    ami_id = config.AMI_ID
    instance_id = config.INSTANCE_ID
    availability_zone = config.AVAILABILITY_ZONE
    instance_type = config.INSTANCE_TYPE
    cpu_usage = get_cpu()
    ram_usage = get_ram()

    data = {
        "app": app,
        "ip_address": ip_address,
        "status": status,
        "port": port,
        "ami_id": ami_id,
        "instance_id": instance_id,
        "availability_zone": availability_zone,
        "instance_type": instance_type,
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
    }

    register(data=data, app=app)


run()
