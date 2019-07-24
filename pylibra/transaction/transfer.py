from pylibra.proto.transaction_pb2 import TransactionArgument
from pylibra.transaction.transaction import CustomTransaction
from pylibra.wallet.account import Account


TRANSFER_OPCODES = "4c49425241564d0a010007014a00000004000000034e000000060000000c54000000050000000d5900000004000000055d0000002900000004860000002000000007a60000000d00000000000001000200010300020002040203020402063c53454c463e0c4c696272614163636f756e74046d61696e0f7061795f66726f6d5f73656e64657200000000000000000000000000000000000000000000000000000000000000000001020004000c000c01110102"


class TransferTransaction(CustomTransaction):
    def __init__(self, receiver, value):
        if isinstance(receiver, Account):
            receiver = receiver.address
        super().__init__(TRANSFER_OPCODES, ["address", "u64"], [receiver, value])
