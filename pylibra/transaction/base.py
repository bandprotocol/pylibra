from pylibra.proto.transaction_pb2 import RawTransaction


class TransactionBase(object):
    def as_raw_transaction(
        self, sender, sequence_number, max_gas_amount, gas_unit_price, expiration_time
    ):
        raw_tx = RawTransaction()
        raw_tx.sender_account = bytes.fromhex(sender)
        raw_tx.sequence_number = sequence_number
        raw_tx.max_gas_amount = max_gas_amount
        raw_tx.gas_unit_price = gas_unit_price
        raw_tx.expiration_time = expiration_time
        self.fill_program(raw_tx.program)
        return raw_tx

    def fill_program(self, program):
        raise NotImplementedError()
