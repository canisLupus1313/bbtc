from enum import Enum

class TcatTLV:
    class Type(Enum):
        COMMAND =        0x00
        RESPONSE =       0x01
        ACTIVE_DATASET = 0x10
        APPLICATION =    0x12
        UNDEFINED =      0xff

        @classmethod
        def from_value(cls, value):
            return cls._value2member_map_.get(value)


    def __init__(self, type: Type = Type.UNDEFINED, data: bytes = bytes()):
        self.type = type
        self.data = data

    def to_bytes(self):
        has_long_header = len(self.data) >= 255
        header_len = 2
        if has_long_header:
            header_len = 4
        len_bytes = len(self.data).to_bytes(header_len - 1, byteorder='big')
        header = bytes([self.type.value]) + len_bytes
        return header + self.data


    @classmethod
    def from_bytes(cls, data):
        res = TcatTLV()
        res.type = TcatTLV.Type.from_value(data[0])
        header_len = 2
        if data[1] == 0xff:
            header_len = 4

        res.data = data[header_len:]
        return res
