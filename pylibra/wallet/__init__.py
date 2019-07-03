from mnemonic import Mnemonic
from sha3 import sha3_256

from pylibra.wallet.account import Account


MNEMONIC = Mnemonic("english")


class LibraWallet(object):
    def __init__(self, words=None, strength=128):
        if words is None:
            words = MNEMONIC.generate(strength)
        self.entropy = MNEMONIC.to_entropy(words)

    def get_account(self, counter):
        shazer = sha3_256()
        shazer.update(self.entropy)
        shazer.update(counter.to_bytes(32, "big"))
        return Account(shazer.digest().hex())

    def to_mnemonic(self):
        return MNEMONIC.to_mnemonic(self.entropy)

