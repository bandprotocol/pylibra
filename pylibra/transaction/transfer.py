from pylibra.proto.transaction_pb2 import TransactionArgument
from pylibra.transaction.base import TransactionBase
from pylibra.wallet.account import Account


TRANSFER_OPCODES = bytes.fromhex(
    "4c49425241564d0a010007014a00000004000000034e000000060000000c54000000050000000d5900000004000000055d0000002900000004860000002000000007a60000000d00000000000001000200010300020002040203020402063c53454c463e0c4c696272614163636f756e74046d61696e0f7061795f66726f6d5f73656e64657200000000000000000000000000000000000000000000000000000000000000000001020004000c000c01110102"
)


class TransferTransaction(TransactionBase):
    def __init__(self, receiver, value):
        if isinstance(receiver, Account):
            receiver = receiver.address

        self.receiver = receiver
        self.value = value

    def fill_program(self, program):
        program.code = TRANSFER_OPCODES
        receiver = program.arguments.add()
        receiver.type = TransactionArgument.ADDRESS
        receiver.data = bytes.fromhex(self.receiver)
        value = program.arguments.add()
        value.type = TransactionArgument.U64
        value.data = self.value.to_bytes(8, "little")
