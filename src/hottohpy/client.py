import logging
import threading
import socket
import time
from .request import CommandMode, Request

# from roombapy.const import MQTT_ERROR_MESSAGES

MAX_CONNECTION_RETRIES = 3


class HottohRemoteClient:
    address = None
    port = None
    log = None
    was_connected = False
    on_connect = None
    on_disconnect = None
    _info = None
    _data = None
    _write_request = False
    _write_parameters = []
    _disconnect_request = False
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, address="192.168.4.10", port=5001):
        """Create tcp client."""
        self.address = address
        self.port = port
        self.log = logging.getLogger(__name__)
        self._thread = threading.Thread(
            target= self.loop, name="hottohpy-client"
        )

    def check(self):
        if self.connect():
            data = self._get_data(command="DAT", parameters=["0"])
            self.socket.close()
            self.was_connected = False
            if len(data) > 0:
                return True
            return False
        return False

    def connect(self):
        attempt = 1
        while attempt <= MAX_CONNECTION_RETRIES:
            self.log.debug(
                "Connecting to %s, attempt %s of %s",
                self.address,
                attempt,
                MAX_CONNECTION_RETRIES,
            )
            try:
                self._open_connection()
                return True
            except Exception as e:
                self.log.error(
                    "Can't connect to %s, error: %s", self.address, e
                )
            attempt += 1

        self.log.error("Unable to connect to %s", self.address)
        return False

    def disconnect(self):
        self._disconnect_request = True

    def _disconnect(self):
        self.socket.close()
        self.was_connected = False
        self._disconnect_request = False

    def _get_data(self, command, parameters):
        request = Request(command=command, parameters=parameters)
        self.socket.send(request.getRequest())
        data = self.socket.recv(1024)
        return self._extractData(f"{data}")

    def _set_data(self, parameters):
        request = Request(command="DAT", mode="W", parameters=parameters)
        self.socket.send(request.getRequest())
        data = self.socket.recv(1024)
        return self._extractData(f"{data}")

    def _open_connection(self):
        if not self.was_connected:
            self.log.debug("Connection was_connected %s", self.was_connected)
            self.socket.connect((self.address, self.port))
            self.was_connected = True
            
            self._thread.daemon = True
            self._thread.start()
            


    def _extractData(self, data):
        # Split data to an array
        return data.split(";")

    def sendCommand(self, parameters):
        self._write_request = True
        self._write_parameters.append(parameters)
        return True

    def loop(self):
        while not self._disconnect_request:
            try:
                # Get info
                self._info = self._get_data("INF", [""])
                # self.log.debug("Information Data %s", self._info)
                # Get Data
                self._data = self._get_data("DAT", ["0"])
                # self.log.debug("Information Data %s", self._data)
                # Write if needed
                while len(self._write_parameters):
                    param = self._write_parameters[0]
                    self.log.debug("Send Command %s", param)
                    res = self._set_data(param)
                    self.log.debug("Get Response command %s", res)
                    self._write_parameters.remove(param)

                self._write_parameters = []
                self._write_request = False
                
                time.sleep(1)
            except socket.error as exc:
                self.log.error("Connection Error : %s", exc)

        self._disconnect()

            

