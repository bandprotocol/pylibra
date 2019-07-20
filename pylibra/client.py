import requests
import time
from io import BytesIO
from grpc import insecure_channel
from sha3 import sha3_256

from pylibra.proto.admission_control_pb2 import SubmitTransactionRequest
from pylibra.proto.admission_control_pb2_grpc import AdmissionControlStub
from pylibra.proto.get_with_proof_pb2 import UpdateToLatestLedgerRequest
from pylibra.proto.transaction_pb2 import SignedTransaction, TransactionArgument
from pylibra.wallet.account import Account
from pylibra.wallet.account_state import AccountState


LIBRA_TESTNET_HOST = "ac.testnet.libra.org:80"
FAUCET_HOST = "http://faucet.testnet.libra.org"
ACCOUNT_STATE_PATH = bytes.fromhex(
    "01217da6c6b3e19f1825cfb2676daecce3bf3de03cf26647c78df00b371b25cc97"
)


class LibraClient(object):
    def __init__(self, channel_uri=LIBRA_TESTNET_HOST, faucet=FAUCET_HOST):
        self.channel = insecure_channel(channel_uri)
        self.stub = AdmissionControlStub(self.channel)
        self.faucet = faucet

    def get_account_states(self, addresses):
        request = UpdateToLatestLedgerRequest()
        for address in addresses:
            if isinstance(address, Account):
                address = address.address

            requested_item = request.requested_items.add()
            requested_item.get_account_state_request.address = bytes.fromhex(address)
        response = self.stub.UpdateToLatestLedger(request)
        results = []
        for response in response.response_items:
            blob = (
                response.get_account_state_response.account_state_with_proof.blob.blob
            )
            buffer = BytesIO(blob)
            blob_len = int.from_bytes(buffer.read(4), byteorder="little")
            key_values = {}
            for idx in range(blob_len):
                key_len = int.from_bytes(buffer.read(4), byteorder="little")
                key = buffer.read(key_len)
                val_len = int.from_bytes(buffer.read(4), byteorder="little")
                val = buffer.read(val_len)
                key_values[key] = val
            if ACCOUNT_STATE_PATH in key_values:
                results.append(AccountState.from_bytes(key_values[ACCOUNT_STATE_PATH]))
            else:
                results.append(None)
        return results

    def get_account_state(self, address):
        return self.get_account_states([address])[0]

    def mint_with_faucet(self, receiver, value):
        if isinstance(receiver, Account):
            receiver = receiver.address

        response = requests.get(
            self.faucet, params={"address": receiver, "amount": value}
        )
        if response.status_code != 200:
            raise Exception(
                "Failed to send request to faucent service: {}".format(self.faucet)
            )
        sequence_number = int(response.content)
        return sequence_number

    def send_transaction(
        self,
        sender,
        transaction,
        max_gas_amount=10000,
        gas_unit_price=0,
        expiration_time=None,
    ):
        account_state = self.get_account_state(sender.address)

        seq = 0
        if account_state:
            seq = account_state.sequence_number

        if expiration_time is None:
            expiration_time = int(time.time()) + 10

        raw_tx = transaction.as_raw_transaction(
            sender.address, seq, max_gas_amount, gas_unit_price, expiration_time
        )
        raw_txn_bytes = raw_tx.SerializeToString()

        shazer = sha3_256()
        shazer.update(
            bytes.fromhex(
                "46f174df6ca8de5ad29745f91584bb913e7df8dd162e3e921a5c1d8637c88d16"
            )
        )
        shazer.update(raw_txn_bytes)

        request = SubmitTransactionRequest()
        signed_txn = request.signed_txn
        signed_txn.sender_public_key = bytes.fromhex(sender.public_key)
        signed_txn.raw_txn_bytes = raw_txn_bytes
        signed_txn.sender_signature = sender.sign(shazer.digest())[:64]
        return self.stub.SubmitTransaction(request)

