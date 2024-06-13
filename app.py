import hashlib
import time
import json
import socket
import threading

# Define the Transaction class
class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

# Define the Block class
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, hash, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.hash = hash
        self.nonce = nonce

# Function to calculate the hash of a block
def calculate_hash(index, previous_hash, timestamp, transactions, nonce):
    value = str(index) + str(previous_hash) + str(timestamp) + str(transactions) + str(nonce)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

# Function to create the genesis block
def create_genesis_block():
    transactions = [Transaction("Genesis", "Genesis", 0)]
    return Block(0, "0", int(time.time()), transactions, calculate_hash(0, "0", int(time.time()), transactions, 0), 0)

# Function to create a new block
def create_new_block(previous_block, transactions):
    index = previous_block.index + 1
    timestamp = int(time.time())
    nonce = 0
    hash = calculate_hash(index, previous_block.hash, timestamp, transactions, nonce)
    while not hash.startswith('0000'):
        nonce += 1
        hash = calculate_hash(index, previous_block.hash, timestamp, transactions, nonce)
    return Block(index, previous_block.hash, timestamp, transactions, hash, nonce)

# Function to check if a chain of blocks is valid
def is_valid_chain(chain):
    previous_block = chain[0]
    for block in chain[1:]:
        if block.previous_hash != calculate_hash(previous_block.index, previous_block.previous_hash, previous_block.timestamp, previous_block.transactions, previous_block.nonce):
            return False
        if not block.hash.startswith('0000'):
            return False
        previous_block = block
    return True

# Define the Wallet class
class Wallet:
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0

# Define the Node class
class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.blockchain = [create_genesis_block()]
        self.peers = []
        self.wallets = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        print(f"Node started on port {self.port}")

    # Function to run the node
    def run(self):
        threading.Thread(target=self.handle_connections).start()

    # Function to handle incoming connections
    def handle_connections(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected by {address}")
            threading.Thread(target=self.handle_client, args=(client,)).start()

    # Function to handle a client connection
    def handle_client(self, client):
        data = client.recv(1024)
        message = json.loads(data.decode())
        if message['type'] == 'new_block':
            block = message['data']
            if is_valid_chain(self.blockchain + [block]):
                self.blockchain.append(block)
                print(f"Block #{block.index} added to the blockchain!")
                print(f"Hash: {block.hash}\\n")
        client.close()

    # Function to broadcast a new block to peers
    def broadcast_new_block(self, block):
        for peer in self.peers:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host, peer))
            client.send(json.dumps({
                'type': 'new_block',
                'data': block.__dict__
            }).encode())
            client.close()

    # Function to create a new wallet
    def create_wallet(self, owner):
        self.wallets[owner] = Wallet(owner)
        print(f"Wallet for {owner} created.")

    # Function to show the balance of a wallet
    def show_wallet(self, owner):
        wallet = self.wallets.get(owner)
        if wallet:
            print(f"{owner}'s wallet balance: {wallet.balance}")
        else:
            print(f"No wallet found for {owner}")

    # Function to create coins for a wallet
    def create_coins(self, owner, amount):
        wallet = self.wallets.get(owner)
        if wallet:
            wallet.balance += amount
            print(f"{amount} coins created for {owner}. New balance: {wallet.balance}")
        else:
            print(f"No wallet found for {owner}")

    # Function to create a transaction
    def create_transaction(self, sender, recipient, amount):
        sender_wallet = self.wallets.get(sender)
        recipient_wallet = self.wallets.get(recipient)
        if sender_wallet and recipient_wallet:
            if sender_wallet.balance >= amount:
                sender_wallet.balance -= amount
                recipient_wallet.balance += amount
                new_transaction = Transaction(sender, recipient, amount)
                block_to_add = create_new_block(self.blockchain[-1], [new_transaction])
                self.blockchain.append(block_to_add)
                self.broadcast_new_block(block_to_add)
                print(f"Transaction from {sender} to {recipient} for {amount} coins has been added to the blockchain!")
            else:
                print(f"Insufficient balance in {sender}'s wallet.")
        else:
            print(f"Wallet not found for sender or recipient.")

    # Function to show all transactions
    def show_all_transactions(self):
        for block in self.blockchain:
            for transaction in block.transactions:
                print(f"Sender: {transaction.sender}, Recipient: {transaction.recipient}, Amount: {transaction.amount}")

# Create a node and run it
node = Node('localhost', 5000)
node.run()

# Create wallets for sender and recipient
node.create_wallet("Account_1")
node.create_wallet("Account_2")

# Show wallets
node.show_wallet("Account_1")
node.show_wallet("Account_2")

# Create coins for sender
node.create_coins("Account_1", 50)

# Show sender's wallet
node.show_wallet("Account_1")

# Create a transaction from sender to recipient
node.create_transaction("Account_1", "Account_2", 10)

# Show all transactions
node.show_all_transactions()

# Check if the blockchain is valid
print("Is blockchain valid?", is_valid_chain(node.blockchain))

# Show wallets after transaction
node.show_wallet("Account_1")
node.show_wallet("Account_2")
