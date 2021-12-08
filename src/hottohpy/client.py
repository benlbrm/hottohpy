import logging
import threading
import socket
import errno
import time
from .request import Request

MAX_CONNECTION_RETRIES = 3


class HottohRemoteClient:
    address = None
    port = None
    _log = None
    _info = None
    _data = None
    _data2 = None
    _raw = None
    _write_request = False
    _write_parameters = []
    _disconnect_request = False
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __is_connected = False
    __end_request = False

    def __init__(self, address="192.168.4.10", port=5001, id=0):
        """Create tcp client."""
        self.id = id
        self.address = address
        self.port = port
        self._log = logging.getLogger(__name__)
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

    def is_connected(self):
        return self.__is_connected

    def _get_data(self, command, parameters):
        request = Request(command=command, parameters=parameters, id=self.id)
        self._socket.send(request.getRequest())
        self._socket.settimeout(60)
        data = self._socket.recv(1024)
        return self._extractData(f"{data}")

    def _set_data(self, parameters):
        request = Request(command="DAT", mode="W", parameters=parameters, id=self.id)
        self._socket.send(request.getRequest())
        self._socket.settimeout(60)
        data = self._socket.recv(1024)
        return self._extractData(f"{data}")
    
    def _set_raw(self, command, mode, parameters):
        request = Request(command=command, mode=mode, parameters=parameters, id=self.id)
        print(request.getRequest())
        self._socket.send(request.getRequest())
        self._socket.settimeout(60)
        data = self._socket.recv(1024)
        print(data)
        return self._extractData(f"{data}")
            
    def _extractData(self, data):
        # Split data to an array
        return data.split(";")

    def sendCommand(self, parameters):
        self._write_request = True
        self._write_parameters.append(parameters)
        return True

    def start(self):
        if not self._thread.is_alive():
            self._log.debug("Start thread to communicate with the stove")
            if self._thread.daemon is not True:
                self._thread.daemon = True
            self._thread.start()

    def stop(self):
        self.__end_request = True

    def loop(self):

        while self.__end_request is False:
            ## Start connection to the stove
            if self.__is_connected is False:
                self.__connect()
            ## if connection ok -> start fetching data's
            ## if not retry forever or until end request

            ## Fetch data
            ## Write data if needed
            if self.__is_connected is True:
                self.__dial()

        ## if end request -> disconnect properly
        ## Disconnect
        self.__disconnect()
           
    def __connect(self):
        try:
            self._log.debug("Try to connect the Stove")
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.address, self.port))
            self.__is_connected = True
        except socket.error as error:
            self.__is_connected = False
            if error.errno == errno.EISCONN:
                self._log.error("Socket already connected to %s", self.address)
                time.sleep(5)
                pass

            self._log.error("Socket error: %s", error)
            time.sleep(5)
            pass
            
    def __dial(self):
        try:
            # self._log.debug("Fetching stove data's")
            # Get info
            self._info = self._get_data("INF", [""])
            # self._log.debug("Information Data %s", self._info)
            # Get Data
            self._data = self._get_data("DAT", ["0"])
            # self._log.debug("Information Data %s", self._data)
            self._data2 = self._get_data("DAT", ["2"])
            # Write if needed
            while len(self._write_parameters):
                param = self._write_parameters[0]
                self._log.debug("Send Command %s", param)
                res = self._set_data(param)
                self._log.debug("Get Response command %s", res)
                self._write_parameters.remove(param)

            self._write_parameters = []
            self._write_request = False
            
            time.sleep(1)

        except socket.error as error:
            self.__is_connected = False
            self._log.error("Dial Error : %s", error)
            pass

    def __disconnect(self):
        self.__is_connected = False
        self._log.debug("Close Stove connection")
        self._socket.close()
