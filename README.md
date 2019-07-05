# PyLibra 🐍

## Summary

PyLibra is an unofficial python client for [Libra blockchain](http://libra.org). The library allows Python program to interact with Libra nodes with [protobuf](https://developers.google.com/protocol-buffers/) message through [grpc](https://grpc.io/). Note that this library performs key management internally. No server required!

## Installation

```sh
$ pip install pylibra
```

## Usage

Below you can find example usages together with explanation. Note that this is an alpha software and interface can change all the time, especially when Libra's interface itself is not yet settle.

### LibraWallet

You can create a wallet using `LibraWallet` class. A wallet is like your masterkey and you can create almost infinitely many Libra accounts from it. Note that PyLibra's mnemonic scheme is not similar to that of [Libra's CLI](https://github.com/libra/libra/tree/master/client/src), so you cannot import mnemonic between the two libraries (yet).

```py
from pylibra import LibraWallet

# Create a new random wallet
wallet1 = LibraWallet()
print(wallet1.to_mnemonic())

# Regenerate wallet from an existing Mnemonic
wallet2 = LibraWallet("student deliver dentist cat gorilla sleep proud naive gown fiber awkward weasel")
print(wallet2.to_mnemonic())
```

### Account

An `Account` can be created by calling `get_account` function on a wallet, with a nonce integer. You use any number (0, 1, 2, ...) to generate a new account under your wallet. This is similar to how [MetaMask](https://metamask.io) keeps track of account. An `Account` contains its `address`, `public_key`, and `private_key`.

```py
from pylibra import LibraWallet

wallet = LibraWallet()

account1 = wallet.get_account(0)
print(account1.address)
print(account1.public_key)
print(account1.private_key)

account2 = wallet.get_account(1)
print(account2.address)
print(account2.public_key)
print(account2.private_key)
```

### LibraClient

A `LibraClient` must be created in order to send protobuf message to a Libra node. You can create a client with the following code.

```py
from pylibra import LibraClient

client1 = LibraClient()  # Default client connecting to the official testnet
client2 = LibraClient('localhost:80')  # Client connecting to a local node
```

### Get Account State of an Address

You can query an account's state by using `get_account_state` function on `LibraClient`. The function returns an `AccountState`, which contains the address' sequence number, balance, and more. If an account has not been created yet (never received any funds), the function will return `None`.

```py
from pylibra import LibraClient, LibraWallet

client = LibraClient()
wallet = LibraWallet("student deliver dentist cat gorilla sleep proud naive gown fiber awkward weasel")
account = wallet.get_account(0)

# You can pass in a hex string address 
account_state = client.get_account_state("4988ceb593200955bf64a024907a94206518d6ac2f624eec569abce38f98da86")
print(account_state.balance)
print(account_state.sequence_number)
print(account_state.received_events_count)
print(account_state.sent_events_count)

# Account object can also be passed
account_state = client.get_account_state(account)
```

### Mint Testnet Libra Token

You can mint testnet libra with `mint_with_faucet` function, which sends a HTTP GET request to [http://faucet.testnet.libra.org](http://faucet.testnet.libra.org). You can customize this URL by passing a key-value argument `faucet` when creating a `LibraClient` (for example, when you want to have your own faucet service). The second argument is the mini-libra amount which is `10^6` times the amount of Libra token. (e.g. `10000` mini-libra is `0.01` Libra token).

```py
from pylibra import LibraClient, LibraWallet

client = LibraClient()
wallet = LibraWallet("student deliver dentist cat gorilla sleep proud naive gown fiber awkward weasel")
account = wallet.get_account(0)

# Mint 0.01 Libra to the given address
client.mint_with_faucet("4988ceb593200955bf64a024907a94206518d6ac2f624eec569abce38f98da86", 10000)  

# Or the given account
client.mint_with_faucet(account, 10000)
```

### Creating a Transfer Transaction Script and Sending the Transaction

Note that in the official testnet, the Libra node ONLY allows sending [the official transfer transaction script](https://github.com/libra/libra/blob/master/language/stdlib/transaction_scripts/peer_to_peer_transfer.mvir). In the future, this libra can be extended to support more transaction scripts as well, as you can see that the logic of creating and sending a transaction is completely independent!

```py
from pylibra import LibraClient, LibraWallet
from pylibra.transaction import TransferTransaction

client = LibraClient()
wallet = LibraWallet("student deliver dentist cat gorilla sleep proud naive gown fiber awkward weasel")
account1 = wallet.get_account(0)
account2 = wallet.get_account(1)

# Create a transfer transaction object to send 0.001 Libra to account2
tx1 = TransferTransaction(account2, 1000)
# Or to send to a plain hex address
tx2 = TransferTransaction("4988ceb593200955bf64a024907a94206518d6ac2f624eec569abce38f98da86", 1000)

# You can send a transaction by calling `send_transaction` function, which takes a sender `Account` and a `Transaction` object. You can also optionally passed `max_gas_amount`, `gas_unit_price`, and `expiration_time`. 
client.send_transaction(account1, tx1)
# Specify gas limit, gas price, and expiration time (this case, it will expire in year 2508)
client.send_transaction(account1, tx2, max_gas_amount=10000, gas_unit_price=0, expiration_time=17000000000)
```

## License

This software is created by [Band Protocol](https://bandprotocol.com) and is released under [the MIT License](https://opensource.org/licenses/MIT).

## Contributing

Any and all contributions are welcome! The process is simple: fork this repo, make your changes, and submit a pull request.

### Running Unit Tests

PyLibra uses [pytest](https://docs.pytest.org/) to run unit tests. 

```
$ PYTHONPATH=. pytest
```
