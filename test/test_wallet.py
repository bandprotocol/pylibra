from pylibra import LibraWallet


def test_create_random_wallet():
    wallet1 = LibraWallet()
    assert len(wallet1.to_mnemonic().split()) == 12
    wallet2 = LibraWallet(strength=256)
    assert len(wallet2.to_mnemonic().split()) == 24
