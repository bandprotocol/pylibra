from mnemonic import Mnemonic
from sha3 import sha3_256

from pylibra.wallet.account import Account


MNEMONIC = Mnemonic("english")


class LibraWallet(object):
    def __init__(self, words):
        self.entropy = MNEMONIC.to_entropy(words)

    def get_account(self, counter):
        shazer = sha3_256()
        shazer.update(self.entropy)
        shazer.update(counter.to_bytes(32, "big"))
        return Account(shazer.digest().hex())

    @staticmethod
    def new(strength=128):
        return LibraWallet(MNEMONIC.generate(strength))

    def to_mnemonic(self):
        return MNEMONIC.to_mnemonic(self.entropy)

