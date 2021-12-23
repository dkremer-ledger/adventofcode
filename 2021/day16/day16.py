from dataclasses import dataclass
from typing import Optional

import base64


def prod(*args):
    k = 1
    for u in args:
        k *= u
    return k


def somme(*args):
    k = 0
    for u in args:
        k += u
    return k


ops = {
    0: somme,
    1: prod,
    2: min,
    3: max,
    5: lambda x, y: int(x > y),
    6: lambda x, y: int(x < y),
    7: lambda x, y: int(x == y),
}


@dataclass
class Packet:
    version: int
    type_id: int
    data: str
    remaining_data: Optional[str] = None


@dataclass
class LiteralPacket(Packet):
    _words: Optional[list] = None
    packets = ()

    def __post_init__(self):
        self._words = []

        for k, c in enumerate(self.data[::5]):
            word = self.data[5 * k : 5 * k + 5]
            self._words.append(word)
            if word.startswith("0"):
                break

        self.remaining_data = self.data[5 * k + 5 :]

        assert all(w[0] == "1" for w in self._words[:-1])
        assert self._words[-1][0] == "0"

        self._words = [w[1:] for w in self._words]

    @property
    def value(self):
        return int("".join(self._words), 2)


@dataclass
class OperatorPacket(Packet):
    subpackets_data: Optional[str] = None
    length_type_id: Optional[str] = None

    def __post_init__(self):
        self.length_type_id = self.data[0]
        self.data = self.data[1:]
        self.packets = []
        self.parse_subpackets()

    def parse_subpackets(self):
        """Parse packets according to the specification given."""
        if self.length_type_id == "0":
            self.subpackets_bit_size = int(self.data[:15], 2)
            self.subpackets_data = self.data[15 : self.subpackets_bit_size + 15]
            self.remaining_data = self.data[self.subpackets_bit_size + 15 :]
            self.parse_type_length_zero()
        elif self.length_type_id == "1":
            self.subpacket_nb_packets = int(self.data[:11], 2)
            self.subpackets_data = self.data[11:]
            self.remaining_data = self.subpackets_data
            self.parse_type_length_one()
        else:
            raise ValueError

    def parse_type_length_zero(self):
        packet = parse_packet(self.subpackets_data)
        self.packets.append(packet)
        while packet.remaining_data:
            packet = parse_packet(packet.remaining_data)
            self.packets.append(packet)

    def parse_type_length_one(self):
        for k in range(self.subpacket_nb_packets):
            packet = parse_packet(self.remaining_data)
            self.packets.append(packet)
            self.remaining_data = packet.remaining_data

    @property
    def value(self):
        op = ops[self.type_id]
        n1, *remaining = list(p.value for p in self.packets)
        return n1 if not remaining else op(n1, *remaining)


def parse_packet(b: str):
    """Basic parse packet function"""
    version = int(b[:3], 2)
    type_id = int(b[3:6], 2)
    b = b[6:]
    if type_id == 4:
        packet = LiteralPacket(version, type_id, b)
    else:
        packet = OperatorPacket(version, type_id, b)
    return packet


input_list = [
    "8A004A801A8002F478",
    "620080001611562C8802118E34",
    "C0015000016115A2E0802F182340",
    "A0016C880162017C3686B18A3D4780",
    (
        "4057231006FF2D2E1AD8025275E4EB45A9ED518E5F1AB4363C60084953FB09E008725772E8ECAC312F0C18025400D"
        "34F732333DCC8FCEDF7CFE504802B4B00426E1A129B86846441840193007E3041483E4008541F8490D4C01A89B0DE"
        "17280472FE937C8E6ECD2F0D63B0379AC72FF8CBC9CC01F4CCBE49777098D4169DE4BF2869DE6DACC015F005C4019"
        "89D0423F0002111723AC289DED3E64401004B084F074BBECE829803D3A0D3AD51BD001D586B2BEAFFE0F1CC80267F"
        "005E54D254C272950F00119264DA7E9A3E9FE6BB2C564F5376A49625534C01B0004222B41D8A80008446A89908800"
        "10A83518A12B01A48C0639A0178060059801C404F990128AE007801002803AB1801A0030A280184026AA8014C01C9"
        "B005CE0011AB00304800694BE2612E00A45C97CC3C7C4020A600433253F696A7E74B54DE46F395EC5E2009C9FF916"
        "89D6F3005AC0119AF4698E4E2713B2609C7E92F57D2CB1CE0600063925CFE736DE04625CC6A2B71050055793B4679"
        "F08CA725CDCA1F4792CCB566494D8F4C69808010494499E469C289BA7B9E2720152EC0130004320FC1D8420008647"
        "E8230726FDFED6E6A401564EBA6002FD3417350D7C28400C8C8600A5003EB22413BED673AB8EC95ED0CE5D480285C"
        "00372755E11CCFB164920070B40118DB1AE5901C0199DCD8D616CFA89009BF600880021304E0EC52100623A4648AB"
        "33EB51BCC017C0040E490A490A532F86016CA064E2B4939CEABC99F9009632FDE3AE00660200D4398CD120401F8C7"
        "0DE2DB004A9296C662750663EC89C1006AF34B9A00BCFDBB4BBFCB5FBFF98980273B5BD37FCC4DF00354100762EC2"
        "58C6000854158750A2072001F9338AC05A1E800535230DDE318597E61567D88C013A00C2A63D5843D80A958FBBBF5"
        "F46F2947F952D7003E5E1AC4A854400404A069802B25618E008667B7BAFEF24A9DD024F72DBAAFCB312002A9336C2"
        "0CE84"
    ),
]


def version_sum(packet, s=0):
    """Return the sum for all versions of the packets"""
    to_inspect = packet.packets
    version = packet.version
    return version + sum(version_sum(p) for p in packet.packets)


def unfold_packets(packet, acc=None):
    """Return the full list of packets flattened (not useful for the exercise)"""
    if acc == None:
        acc = []
    acc.append(packet)
    for p in packet.packets:
        unfold_packets(p, acc)
    return acc


if __name__ == "__main__":
    for data in input_list[:]:
        packet = parse_packet(
            "".join("{:08b}".format(c) for c in base64.b16decode(data)).rstrip("0")
        )
        print("version sum:", version_sum(packet), "packet value:", packet.value)
