from io import BytesIO


class AccountState(object):
    def __init__(
        self, authentication_key, balance, received_events_count, sent_events_count, sequence_number
    ):
        self.authentication_key = authentication_key
        self.balance = balance
        self.received_events_count = received_events_count
        self.sent_events_count = sent_events_count
        self.sequence_number = sequence_number

    @staticmethod
    def empty(address):
        return AccountState(address, 0, 0, 0, 0)

    @staticmethod
    def from_bytes(data):
        buffer = BytesIO(data)
        authentication_key_len = int.from_bytes(buffer.read(4), byteorder="little")
        authentication_key = buffer.read(authentication_key_len).hex()
        balance = int.from_bytes(buffer.read(8), byteorder="little")
        received_events_count = int.from_bytes(buffer.read(8), byteorder="little")
        sent_events_count = int.from_bytes(buffer.read(8), byteorder="little")
        sequence_number = int.from_bytes(buffer.read(8), byteorder="little")
        return AccountState(
            authentication_key, balance, received_events_count, sent_events_count, sequence_number
        )

    def __str__(self):
        return "AccountState({}, {}, {}, {}, {})".format(
            self.authentication_key,
            self.balance,
            self.received_events_count,
            self.sent_events_count,
            self.sequence_number,
        )

