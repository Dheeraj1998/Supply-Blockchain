# Importing the required libraries
import hashlib as hasher
import datetime as date
import pickle

# Global variables
supply_blockchain = []

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
	def __init__(self, supplier_pk, receiver_pk, item_id, timestamp, signature):
		self.supplier_pk = supplier_pk
		self.receiver_pk = receiver_pk
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
	print('\n')
	for block in supply_blockchain:
		print('------------------------------')
		print(block.index)
		print(block.timestamp)
		print(block.supply_data)
		print(block.previous_hash)
	print('------------------------------')

view_blockchain()

