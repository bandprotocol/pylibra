from mnemonic import Mnemonic


MNEMONIC = Mnemonic("english")


class LibraWallet(object):
    @staticmethod
    def new(strength=128):
        return LibraWallet(MNEMONIC.generate(strength))

    def __init__(self, words):
        self.entropy = MNEMONIC.to_entropy(words)

    def to_mnemonic(self):
        return MNEMONIC.to_mnemonic(self.entropy)

