# Importing the required libraries
import hashlib as hasher
import datetime as date

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Signature import pkcs1_15

import random
import time

# Global variables
supply_blockchain = []
utxo_array = []
manufacturers_list = []
other_users_list = []
global_index = 0
pow_proof = int(0)

class Supply_Block:
	
	# The initialisation function allows the setting up of a block
	def __init__(self, index, timestamp, supply_data, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.supply_data = supply_data
		self.previous_hash = previous_hash
		self.proof_of_work = int(generate_pow())
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
	initial_start = pow_proof + 1
	
	while(1):
		sha = hasher.sha256()
		sha.update(str(initial_start).encode('utf-8'))
		hash_value = sha.hexdigest()
		initial_start = int(initial_start) + 1
		
		if(hash_value[0] == '0' and hash_value[1] == '0' and hash_value[2] == '0' and hash_value[-1] == '0' and hash_value[-2] == '0'):
			end_time = time.time()
			pow_proof = initial_start - 1
			print('\nThe required hash value is: ' + hash_value)
			print('The PoW number is: ' + str(pow_proof))
			print('The total time taken is: ' + str((end_time - start_time)))
			
			break
	
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
def make_transaction(supplier_key, receiver_key, item_id):
	
	# Selection functions for the keys and the item ID
	selection = input('\nSelect type of key (M/O) for supplier: ')
	if selection == 'M':
		index = int(input('There are a total of ' + str(len(manufacturers_list)) + ' users. Enter your selection: ')) - 1
		supplier_key = manufacturers_list[index]
		
	elif selection == 'O':
		index = int(input('There are a total of ' + str(len(other_users_list)) + ' users. Enter your selection: ')) - 1
		supplier_key = other_users_list[index]
		
	selection = input('\nSelect type of key (M/O) for receiver: ')
	if selection == 'M':
		index = int(input('There are a total of ' + str(len(manufacturers_list)) + ' users. Enter your selection: ')) - 1
		receiver_key = manufacturers_list[index]
		
	elif selection == 'O':
		index = int(input('There are a total of ' + str(len(other_users_list)) + ' users. Enter your selection: ')) - 1
		receiver_key = other_users_list[index]
	
	receiver_puk = receiver_key.publickey().exportKey("PEM").decode('utf-8')
	item_id = input('Enter the ID of the tracked item: ')
	
	# Acquiring the details for the transactions
	supplier_puk = supplier_key.publickey()
	timestamp = date.datetime.now()
	
	# Generating the message text and the signature
	message = str(supplier_puk.exportKey("PEM").decode('utf-8')) + str(receiver_puk) + item_id + str(timestamp)
	hash_message = SHA256.new(message.encode('utf-8'))
	
	supplier_prk = RSA.import_key(supplier_key.exportKey("DER"))
	signature = pkcs1_15.new(supplier_prk).sign(hash_message)
	
	# Creating a new transaction
	new_transaction = Transaction(supplier_puk, receiver_puk, item_id, timestamp, signature)
	utxo_array.append(new_transaction)

# The function for mining the block in the supply blockchain
def mine_block():
	global global_index
	max_range = len(utxo_array)
	transaction_amount = random.randint(0, max_range)
	transaction_array = []
	
	print('\nThe number of selected transactions for the block is: ' + str(transaction_amount))
	
	if(transaction_amount):
		for index in range(0, transaction_amount):
			# All verifications for the transactions
			if(verify_transaction(utxo_array[0])):
				print('\nThe sign verification for transaction #' + str(index + 1) + ' was true!')
				if(check_item_code(utxo_array[0])):
					print('The item code has been found. Checking the previous owner details.')
					if(check_previous_owner(utxo_array[0])):
						print('Verification of previous owner has been done!')
						transaction_array.append(utxo_array[0])
					else:
						print('Verification of previous owner has failed!')
				else:
					print('The item code was not found on blockchain. Checking for manufacturer credentials.')
					if(check_manufacturer_credentials(utxo_array[0])):
						print('The new item has been added under the manufacturer.')
						transaction_array.append(utxo_array[0])
					else:
						print('The transaction key is not authorised as a manufacturer!')
			else:
				print('The sign verification for transaction #' + str(index + 1) + ' was false!')
			utxo_array.pop(0)
		
		if(len(transaction_array) != 0):
			new_block = Supply_Block(global_index, date.datetime.now(), transaction_array, supply_blockchain[global_index - 1].hash)
			global_index = global_index + 1
			supply_blockchain.append(new_block)
		
	else:
		# Prevent addition of blocks with no transactions
		print('No transactions have been selected and therefore no block has been added!')

# This function is used for the verifying the signature of the transaction
def verify_transaction(self):
	supplier_puk = RSA.import_key(self.supplier_puk.exportKey("DER"))
	
	message = str(self.supplier_puk.exportKey("PEM").decode('utf-8')) + str(self.receiver_puk) + self.item_id + str(self.timestamp)
	hash_message = SHA256.new(message.encode('utf-8'))
	
	try:
		pkcs1_15.new(supplier_puk).verify(hash_message, self.signature)
		return True
	except (ValueError, TypeError):
		return False
	
# Smart contract for checking if the input item code is avaiable on the blockchain & checking the previous owner of the consignment
def check_item_code(self):
	found_flag = False
	temp_blockchain = supply_blockchain[::-1]
	
	for block in temp_blockchain[:-1:]:
		for transaction in block.supply_data:
			if(transaction.item_id == self.item_id):
				found_flag = True
	
	return found_flag
	
# Smart contract for checking the previous owner of the commodity
def check_previous_owner(self):
	found_flag = False
	temp_blockchain = supply_blockchain[::-1]
	
	for block in temp_blockchain[:-1:]:
		for transaction in block.supply_data:
			if(transaction.item_id == self.item_id):
				if(transaction.receiver_puk == self.supplier_puk.exportKey("PEM").decode('utf-8')):
					return True
				else:
					return False

# Smart contract for checking if the user is an authorised manufacturer
def check_manufacturer_credentials(self):
	for item in manufacturers_list:
		if str(self.supplier_puk.exportKey("PEM").decode('utf-8')) == str(item.publickey().exportKey("PEM").decode('utf-8')):
			return True
	
	return False

# The function would verify all the blocks in the given blockchain
def verify_blockchain():
	previous_block = supply_blockchain[0]
	count = 1
	
	for block in supply_blockchain[1:]:
		print('\nFor the block #' + str(count) + ': ')
		for transaction in block.supply_data:
			print('The item ID is ' + str(transaction.item_id) + ' and the associated timestamp is ' + str(transaction.timestamp))
		
		if(str(previous_block.hash) == str(block.previous_hash)):
			print('The hash values have been verified.')
		
		sha = hasher.sha256()
		sha.update(str(int(block.proof_of_work)).encode('utf-8'))
		hash_value = sha.hexdigest()
		print('The PoW number is ' + str(block.proof_of_work) + ' and the associated hash is ' + hash_value)
		
	print('------------------------------------------------------------------------------------------------------------------------')
	print('\n\n')

# Function for generating manufacturer keys
def generate_manufacturer_keys(number):
	for item in range(0, int(number)):
		manufacturers_list.append(RSA.generate(1024, Random.new().read))
	#print(manufacturers_list)
	print('\nThe manufacturer keys have been generated.')
	
# Function for generating stakeholder keys
def generate_other_keys(number):
	for item in range(0, int(number)):
		other_users_list.append(RSA.generate(1024, Random.new().read))
	#print(other_users_list)
	print('\nThe stakeholder keys have been generated.')
	
# Function for tracking an item
def track_item(item_code):
	not_found_flag = True
	
	for block in supply_blockchain[1:]:
		for transaction in block.supply_data:
			if(item_code == transaction.item_id):
				if(not_found_flag):
					print('\nThe item (' + item_code + ') has been found and the tracking details are: ')
					not_found_flag = False
				
				manufacturer_suppplier = False
				manufacturer_receiver = False
				
				supplier_count = 0
				supplier_not_found_flag = True
				
				for item in manufacturers_list:
					supplier_count = supplier_count + 1
					
					if str(transaction.supplier_puk.exportKey("PEM").decode('utf-8')) == str(item.publickey().exportKey("PEM").decode('utf-8')):
							supplier_not_found_flag = False
							manufacturer_suppplier = True
							break
				
				if(supplier_not_found_flag):
					supplier_count = 0
					
					for item in other_users_list:
						supplier_count = supplier_count + 1
					
						if str(transaction.supplier_puk.exportKey("PEM").decode('utf-8')) == str(item.publickey().exportKey("PEM").decode('utf-8')):
							supplier_not_found_flag = False
							break
				
				receiver_count = 0
				receiver_not_found_flag = True
				
				for item in manufacturers_list:
					receiver_count = receiver_count + 1
					
					if str(transaction.receiver_puk) == str(item.publickey().exportKey("PEM").decode('utf-8')):
							receiver_not_found_flag = False
							manufacturer_receiver = True
							break
				
				if(receiver_not_found_flag):
					receiver_count = 0
					
					for item in other_users_list:
						receiver_count = receiver_count + 1
					
						if str(transaction.receiver_puk) == str(item.publickey().exportKey("PEM").decode('utf-8')):
							receiver_not_found_flag = False
							break
				
				final_result = ""
				
				if(manufacturer_suppplier):
					final_result = final_result + "Manufacturer #" + str(supplier_count) + " transferred the asset to "
				else:
					final_result = final_result + "Stakeholder #" + str(supplier_count) + " transferred the asset to "

				if(manufacturer_receiver):
					final_result = final_result + "Manufacturer #" + str(receiver_count) + " at " + str(transaction.timestamp)
				else:
					final_result = final_result + "Stakeholder #" + str(receiver_count) + " at " + str(transaction.timestamp)
				
				print(final_result)
				
	if(not_found_flag):
		print('\nThe item code was not found in the blockchain.')

# Generating keys for manufactures and other users
number_manufacturers = int(input('\nEnter the number of manufacturers: '))
generate_manufacturer_keys(number_manufacturers)
	
number_other_users = int(input('\nEnter the number of stakeholders: '))
generate_other_keys(number_other_users)

# Inserting a genesis block into blockchain
supply_blockchain.append(create_genesis_block())
print('\n\nWelcome to the supply blockchain.')

# Menu driven program for the supply blockchain
while(1):
	print('\nThe following options are available to the user: ')
	print('1. View the blockchain. ')
	print('2. Enter a transaction. ')
	print('3. View the UTXO array. ')
	print('4. Mine a block. ')
	print('5. Verify the blockchain. ')
	print('6. Generate RSA keys. ')
	print('7. Track an item.')
	print('8. Exit.')
	
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
	elif(choice == 6):
		number_manufacturers = int(input('\nEnter the number of manufacturers: '))
		generate_manufacturer_keys(number_manufacturers)
		number_other_users = int(input('Enter the number of stakeholders: '))
		generate_other_keys(number_other_users)
	elif(choice == 7):
		item_code = input('Enter the item code: ')
		track_item(item_code)
	elif(choice == 8):
		break
	else:
		print('This is an invalid option.')
