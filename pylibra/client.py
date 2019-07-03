import requests
from io import BytesIO
from grpc import insecure_channel

from pylibra.proto.admission_control_pb2_grpc import AdmissionControlStub
from pylibra.proto.get_with_proof_pb2 import UpdateToLatestLedgerRequest
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

    def mint_with_faucet(self, receiver, value):
        response = requests.get(self.faucet, params={"address": receiver, "amount": value})
        if response.status_code != 200:
            raise Exception("Failed to send request to faucent service: {}".format(self.faucet))
        sequence_number = int(response.content)
        return sequence_number

    def get_account_states(self, addresses):
        request = UpdateToLatestLedgerRequest()
        for address in addresses:
            requested_item = request.requested_items.add()
            requested_item.get_account_state_request.address = bytes.fromhex(address)
        response = self.stub.UpdateToLatestLedger(request)
        results = []
        for response in response.response_items:
            blob = response.get_account_state_response.account_state_with_proof.blob.blob
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
        return results

    def get_account_state(self, address):
        return self.get_account_states([address])[0]
