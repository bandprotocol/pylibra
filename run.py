from io import BytesIO
from grpc import insecure_channel

from pylibra.proto.admission_control_pb2_grpc import AdmissionControlStub
from pylibra.proto.get_with_proof_pb2 import UpdateToLatestLedgerRequest


from pylibra.client import LibraClient

c = LibraClient()
print(c.get_account_state("659f81bf3e938eda17ae5bf5c7b5589d9320fdcf93660f7b63b501c46738dc83"))
# print(
#     c.mint_with_faucet("659f81bf3e938eda17ae5bf5c7b5589d9320fdcf93660f7b63b501c46738dc83", 10000000)
# )

from pylibra.transaction.transfer import TransferTransaction

t = TransferTransaction("659f81bf3e938eda17ae5bf5c7b5589d9320fdcf93660f7b63b501c46738dc83", 10)
print(
    t.as_raw_transaction(
        "659f81bf3e938eda17ae5bf5c7b5589d9320fdcf93660f7b63b501c46738dc83", 1, 1, 1, 1
    )
)

# channel = insecure_channel("ac.testnet.libra.org:80")
# stub = AdmissionControlStub(channel)


# request = UpdateToLatestLedgerRequest()
# requested_item = request.requested_items.add()
# requested_item.get_account_state_request.address = bytes.fromhex(
#     "659f81bf3e938eda17ae5bf5c7b5589d9320fdcf93660f7b63b501c46738dc83"
# )


# response = stub.UpdateToLatestLedger(request)

# AccountStatePath = "01217da6c6b3e19f1825cfb2676daecce3bf3de03cf26647c78df00b371b25cc97"

# from pylibra.wallet.account_state import AccountState

# for response in response.response_items:
#     print(dir(response))
#     blob = response.get_account_state_response.account_state_with_proof.blob.blob
#     print(blob.hex())

#     buffer = BytesIO(blob)
#     blob_len = int.from_bytes(buffer.read(4), byteorder="little")

#     for idx in range(blob_len):
#         key_len = int.from_bytes(buffer.read(4), byteorder="little")
#         key = buffer.read(key_len).hex()
#         val_len = int.from_bytes(buffer.read(4), byteorder="little")
#         # val = buffer.read(val_len).hex()
#         # print(key_len, val_len)
#         # print(key, val)
#         print(AccountState.from_buffer(buffer))

#     # .get_account_state_with_proof)
