from pylibra.proto.transaction_pb2 import TransactionArgument
from pylibra.transaction.base import TransactionBase
from pylibra.wallet.account import Account


class CustomTransaction(TransactionBase):
    def __init__(self, opcodes, arg_types, arg_vals):
        self.opcodes = opcodes
        self.arg_types = arg_types
        self.arg_vals = arg_vals

    def fill_program(self, program):
        program.code = bytes.fromhex(self.opcodes)
        for kind, val in zip(self.arg_types, self.arg_vals):
            arg = program.arguments.add()
            if kind.lower() == "address":
                if isinstance(val, Account):
                    val = val.address
                arg.type = TransactionArgument.ADDRESS
                arg.data = bytes.fromhex(val)
            elif kind.lower() == "u64":
                arg.type = TransactionArgument.U64
                arg.data = val.to_bytes(8, "little")
            else:
                raise ValueError("Unknown arg type: {}".format(kind))

