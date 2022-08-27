from ip2geotools.databases.noncommercial import DbIpCity
from dolphin.metrics import EventLogging
from dolphin.metrics.clientevent import ClientEvent


def client_event(ip_address):
    eventlogger = EventLogging()
    if ip_address == "127.0.0.1":
        ip_address = "73.144.225.249"
    response = DbIpCity.get(ip_address=ip_address, api_key="free")
    eventlogger.save_event(
        ClientEvent(ip_address=ip_address, latitude=response.latitude, longitude=response.longitude)
    )
