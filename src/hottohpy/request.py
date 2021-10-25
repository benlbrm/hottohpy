from enum import Enum

import crcmod.predefined


class Command(Enum):
    DAT = "DAT"


class CommandMode(Enum):
    READ = "R"
    WRITE = "W"
    EXECUTE = "E"


IdSocket = 0


class Request:
    def __init__(self, command="DAT", mode="R", parameters=["0"], id=0):
        """Generate communication frame"""
        self.command = command
        self.mode = mode
        self.parameters = parameters
        self.id = id
        # self.socketId = 1
        self.request = ""
        self._buildRawPacket()

    def _buildRawPacket(self):
        """Buld raw packet from data"""
        strSocketId = str(self.id).zfill(5)
        strRawData = self._getRawData()
        strData = strSocketId + "A---" + strRawData
        strCrc = self._getCrc(strData)
        self.request = "#" + strData + strCrc + "\n"

    def _getRawData(self):
        lenParameters = f"{len(self._getParameters()):0>4X}"
        strCmd = lenParameters + self.command + self.mode
        return strCmd + self._getParameters()

    def _getParameters(self):
        str1 = ""
        for value in self.parameters:
            str1 += value + ";"

        return str1

    def _getCrc(self, message):
        crc16 = crcmod.predefined.Crc("crc-ccitt-false")
        crc16.update(message.encode("utf-8"))
        return crc16.hexdigest()

    def getRequest(self):
        return self.request.encode("utf-8")
