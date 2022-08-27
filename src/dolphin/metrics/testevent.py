from datetime import datetime
import time
from time import sleep
from dolphin.metrics.influxevent import InfluxEvent


class TestEvent(InfluxEvent):
    def __init__(self, event_type=None):
        super(TestEvent, self).__init__(event_type=event_type)
        self.count = 1
        self.source = "test"
        t = time.perf_counter()
        sleep(0.3)
        self.response_time = time.perf_counter() - t
        self.summons_time = datetime.now()

    def get_influx_event(self):
        event = super().get_influx_event()
        event[0]["fields"]["count"] = self.count
        event[0]["fields"]["response_time"] = self.response_time
        event[0]["summons_time"] = self.summons_time
        event[0]["tags"]["source"] = self.source
        return event
