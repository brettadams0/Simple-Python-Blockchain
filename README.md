# Simple Python Blockchain

This repository contains a simple implementation of a blockchain in Python. It includes the basic components of a blockchain such as transactions, blocks, wallets, and nodes.

## Features

- Transaction Class: Represents a transaction in the blockchain.
- Block Class: Represents a block in the blockchain.
- Wallet Class: Represents a wallet for a user.
- Node Class: Represents a node in the network.

## Usage

**1. Create a node and run it:**

node = Node('localhost', 5000)
node.run()

**2. Create wallets for sender and recipient:**

node.create_wallet("Account_1")
node.create_wallet("Account_2")

**3. Show wallets:**

node.show_wallet("Account_1")
node.show_wallet("Account_2")

**4. Create coins for sender:**

node.create_coins("Account_1", 50)

**5. Show sender’s wallet:**

node.show_wallet("Account_1")

**6. Create a transaction from sender to recipient:**

node.create_transaction("Account_1", "Account_2", 10)

**7. Show all transactions:**

node.show_all_transactions()

**8. Check if the blockchain is valid:**

print("Is blockchain valid?", is_valid_chain(node.blockchain))

**9. Show wallets after transaction:**

node.show_wallet("Account_1")
node.show_wallet("Account_2")
