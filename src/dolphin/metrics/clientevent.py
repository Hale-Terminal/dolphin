from dolphin.metrics import InfluxEvent


class ClientEvent(InfluxEvent):
    def __init__(self, ip_address, latitude, longitude, event_type=None):
        super(ClientEvent, self).__init__(event_type=event_type)
        self.ip_address = ip_address
        self.latitude = latitude
        self.longitude = longitude

    def get_influx_event(self):
        event = super().get_influx_event()
        event[0]["fields"]["latitude"] = self.latitude
        event[0]["fields"]["longitude"] = self.longitude
        event[0]["tags"]["client_ip"] = self.ip_address
        return event
