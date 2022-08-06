import logging
import socket

import requests

from .config import GUARDIAN_SERVERS

log = logging.getLogger(__file__)


class Metrics(object):
    def __init__(self):
        pass

    def gauge(self, name, value, tags=None):
        pass

    def counter(self, name, value=None, tags=None):
        """
        name = server.call.counter

        tags = {
            method: method,
            endpoint: endpoint,
            status_code: status_code
        }
        """
        data = {"name": name, "value": value, "tags": tags}
        self._send(data=data)

    def timer(self, name, value, tags=None):
        """
        name = server.call.counter

        value = elapsed_time

        tags = {
            method: method,
            endpoint: endpoint,
            status_code: status_code
        }

        """
        data = {"name": name, "value": value, "tags": tags}
        self._send(data=data)

    def _send(self, data: dict):
        hostname = socket.gethostname()
        data.update({"hostname": hostname})

        log.debug("Sending metrics to Guardian server....")
        try:
            for guardian in GUARDIAN_SERVERS:
                try:
                    r = requests.post(guardian, data=data)
                    if r.status_code == 200:
                        log.debug(f"Successfully sent metrics to {guardian}")
                        break
                    log.debug(
                        f"Failed to send metrics to {guardian}. Status Code: {r.status_code}. Trying next server"
                    )
                    continue
                except Exception as e:
                    log.debug(
                        f"Failed to send metrics to {guardian}. Reason: {e}. Trying next server"
                    )
                    continue
        except Exception as e:
            log.debug(f"Failed to send metrics to any guardian server. Reason: {e}")


provider = Metrics()
