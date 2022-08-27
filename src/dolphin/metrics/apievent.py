from dolphin.metrics import InfluxEvent


class APIEvent(InfluxEvent):
    def __init__(
        self, method, endpoint, response_time, status_code, status, client_ip, event_type=None
    ):
        super(APIEvent, self).__init__(event_type=event_type)
        self.method = method
        self.endpoint = endpoint
        self.counter = 1
        self.response_time = response_time
        self.status_code = status_code
        self.status = status
        self.client_ip = client_ip

    def get_influx_event(self):
        event = super().get_influx_event()
        event[0]["fields"]["response_time"] = self.response_time
        event[0]["fields"]["count"] = self.counter
        event[0]["fields"]["method"] = self.method
        event[0]["fields"]["status_code"] = self.status_code
        event[0]["fields"]["status"] = self.status
        event[0]["tags"]["client_ip"] = self.client_ip
        event[0]["tags"]["endpoint"] = self.endpoint
        return event
