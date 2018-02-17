# Importing the required libraries
import hashlib as hasher
import datetime as date
import pickle
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import json
import random
import time

# Global variables
supply_blockchain = []
utxo_array = []
global_index = 0
pow_proof = 0

class Supply_Block:
	
	# The initialisation function allows the setting up of a block
	def __init__(self, index, timestamp, supply_data, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.supply_data = supply_data
		self.previous_hash = previous_hash
		self.proof_of_work = generate_pow()
		self.hash = self.hash_block()
		
	# The hashing function for the block using SHA 256
	def hash_block(self):
		sha = hasher.sha256()
		
		sha.update((str(self.index) + 
               str(self.timestamp) + 
               str(self.supply_data) + 
               str(self.previous_hash)).encode('utf-8'))
               
		return sha.hexdigest()
		
# Algorithm for generating a proof-of-work (based on bitcoin PoW)
# The algorithm requires to find SHA256 of a natural number (string) such that has the first three positions as '000' and ends with '00'
def generate_pow():
	start_time = time.time()
	global pow_proof
	
	sha = hasher.sha256()
	initial_start = pow_proof
	
	while(1):
		sha.update(str(initial_start).encode('utf-8'))
		hash_value = sha.hexdigest()
		
		if(hash_value[0] == '0' and hash_value[1] == '0' and hash_value[2] == '0' and hash_value[-1] == '0' and hash_value[-2] == '0'):
			end_time = time.time()
			pow_proof = initial_start
			print('\nThe required hash value is: ' + hash_value)
			print('The PoW number is: ' + str(pow_proof))
			print('The total time taken is: ' + str((end_time - start_time)))
			break
		
		initial_start = initial_start + 1
	
	return pow_proof

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
	global global_index 
	global_index = global_index + 1
	print('\n\nThe genesis block is being created.')
	
	return Supply_Block(0, date.datetime.now(), "GENESIS BLOCK", "0")

# This function is used for viewing all the blocks and the transactions in the blockchain
def view_blockchain():
	print('\n\nThe list of blocks are: \n')
	for block in supply_blockchain:
		print('\n------------------------------------------------------------------------------------------------------------------------')
		print(block.index)
		print(block.timestamp)
		print(block.supply_data)
		print(block.proof_of_work)
		print(block.hash)
		print(block.previous_hash)
	print('------------------------------------------------------------------------------------------------------------------------')
	print('\n\n')
	
# This function is used to view all the Unspend Transaction Outputs
def view_UTXO():
	print('\n\nThe list of UTXO are: \n')
	for transaction in utxo_array:
		print('\n------------------------------------------------------------------------------------------------------------------------')
		print(transaction.supplier_puk.exportKey("PEM").decode('utf-8'))
		print(transaction.receiver_puk)
		print(transaction.item_id)
		print(transaction.timestamp)
		print(transaction.signature)
	print('------------------------------------------------------------------------------------------------------------------------')
	print('\n\n')

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

# The function for mining the block in the supply blockchain
def mine_block():
	global global_index
	max_range = len(utxo_array)
	transaction_amount = random.randint(0, max_range)
	transaction_array = []
	
	print('\nThe number of selected transactions for the block is: ' + str(transaction_amount))
	
	if(transaction_amount):
		for index in range(0, transaction_amount):
			if(verify_transaction(utxo_array[0])):
				print('The verification for transaction #' + str(index + 1) + ' was true!')
				transaction_array.append(utxo_array[0])
			else:
				print('The verification for transaction #' + str(index + 1) + ' was false!')
			utxo_array.pop(0)
			
		new_block = Supply_Block(global_index, date.datetime.now(), transaction_array, supply_blockchain[global_index - 1].hash)
		global_index = global_index + 1
		supply_blockchain.append(new_block)
		
	else:
		# Prevent addition of blocks with no transactions
		print('No transactions have been selected and therefore no block has been added!')

# Inserting a genesis block into blockchain
supply_blockchain.append(create_genesis_block())

# Menu driven program for the supply blockchain
while(1):
	print('\nWelcome to the supply blockchain. The following options are available to the user: ')
	print('1. View the blockchain. ')
	print('2. Generate a transaction. ')
	print('3. View the UTXO array. ')
	print('4. Mine a block. ')
	print('5. Verify the blockchain. ')
	print('6. Exit.')
	
	choice = int(input('Enter your choice: '))
	
	if(choice == 1):
		view_blockchain()
	elif(choice == 2):
		make_transaction('','','')
	elif(choice == 3):
		view_UTXO()
	elif(choice == 4):
		mine_block()
	elif(choice == 5):
		verify_blockchain()
	else:
		break
