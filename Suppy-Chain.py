# Importing the required libraries
import hashlib as hasher
import datetime as date
import pickle
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import json

# Global variables
supply_blockchain = []
utxo_array = []

class Supply_Block:
	
	# The initialisation function allows the setting up of a block
	def __init__(self, index, timestamp, supply_data, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.supply_data = supply_data
		self.previous_hash = previous_hash
		self.hash = self.hash_block()
		
	# The hashing function for the block using SHA 256
	def hash_block(self):
		sha = hasher.sha256()
		
		sha.update((str(self.index) + 
               str(self.timestamp) + 
               str(self.supply_data) + 
               str(self.previous_hash)).encode('utf-8'))
               
		return sha.hexdigest()

class Transaction:
	
	# The initialisation function for a single transaction
	def __init__(self, supplier_puk, receiver_puk, item_id, timestamp, signature):
		self.supplier_puk = supplier_puk
		self.receiver_puk = receiver_puk
		self.item_id = item_id
		self.timestamp = timestamp
		self.signature = signature

# This function is used to create genesis block
def create_genesis_block():
	return Supply_Block(0, date.datetime.now(), "GENESIS BLOCK", "0")

# Inserting a genesis block into blockchain
supply_blockchain.append(create_genesis_block())	

# This function is used for viewing all the blocks and the transactions in the blockchain
def view_blockchain():
	print('\n\nThe list of blocks are: \n')
	for block in supply_blockchain:
		print('------------------------------')
		print(block.index)
		print(block.timestamp)
		print(block.supply_data)
		print(block.previous_hash)
	print('------------------------------')
	print('\n')
	
# This function is used to view all the Unspend Transaction Outputs
def view_UTXO():
	print('\n\nThe list of UTXO are: \n')
	for transaction in utxo_array:
		print('------------------------------')
		print(transaction.supplier_puk.exportKey("PEM").decode('utf-8'))
		print(transaction.receiver_puk)
		print(transaction.item_id)
		print(transaction.timestamp)
		print(transaction.signature)
	print('------------------------------')
	print('\n')

# This function is used to generate a transaction
def make_transaction(supplier_key, receiver_puk, item_id):
	
	# Generator functions for the keys and the other data
	random_generator = Random.new().read
	supplier_key = RSA.generate(1024, random_generator)
	# print(supplier_key.exportKey().decode('utf-8'))
	receiver_puk = RSA.generate(1024, random_generator)
	# print(receiver_puk.exportKey().decode('utf-8'))
	# print(receiver_puk.publickey().exportKey("PEM").decode('utf-8'))
	receiver_puk = receiver_puk.publickey().exportKey("PEM").decode('utf-8')
	item_id = '1'
	
	# Acquiring the details for the transactions
	supplier_puk = supplier_key.publickey()
	timestamp = date.datetime.now()
	
	# Generating the message text and the signature
	message = str(supplier_puk.exportKey("PEM").decode('utf-8')) + str(receiver_puk) + item_id + str(timestamp)
	hash_message = SHA256.new(message.encode('utf-8')).digest()
	signature = supplier_key.sign(hash_message, '')
	
	# Creating a new transaction
	new_transaction = Transaction(supplier_puk, receiver_puk, item_id, timestamp, signature)
	utxo_array.append(new_transaction)

# This function is used for the verifying the signature of the transaction
def verify_transaction(self):
	message = str(self.supplier_puk.exportKey("PEM").decode('utf-8')) + str(self.receiver_puk) + self.item_id + str(self.timestamp)
	hash_message = SHA256.new(message.encode('utf-8')).digest()
	
	return self.supplier_puk.verify(hash_message, self.signature)
	
view_blockchain()
make_transaction('a','a','a')
view_UTXO()
verify_transaction(utxo_array[0])
