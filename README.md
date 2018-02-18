# Supply-Blockchain
Blockchain has become a trending topic with the increasing interest of public in crypto-currency such as Bitcoin :moneybag:. This project demonstrates a use-case of blockchain in IoT. This use-case is based on the [Christidis, K. and Devetsikiotis, M., 2016. Blockchains and smart contracts for the internet of things. IEEE Access, 4, pp.2292-2303.](http://ieeexplore.ieee.org/abstract/document/7467408/)

# Asset Tracking
Compared to the traditional tracking, a blockchain network that is set up to track this asset would mean that there is only a single shared database to keep track of, where updates come with cryptographic verifiability, get propagated along the network automatically, and create an auditable trail of information. This allows to prevent disputes between the different parties. 

# Architecture Diagram
The concept could be understood from the below picture:
![Architecture Diagram](images/architecture-diagram.png)

# Development
The program looks at the functionality that is mandatory for a asset tracking blockchain. The program has been developed on [Python 3.6.1](https://www.python.org/downloads/release/python-361/)

# Usage
1. Run `python3 Supply-Blockchain.py` in the downloaded directory.
2. The number of manufacturer and stakeholder keys need to be specified.
3. The genesis block is generated and the menu is shown to the user.
4. The transactions can be added according to the shipment movement.
5. The mining process selects a random number of transactions to be verified during each run.

# Functionalities
* `View blockchain` - This allows the user to view the entire blockchain structure.
* `Enter transaction` - This allows the user to enter new transactions to the UTXO.
* `View UTXO` - This views the entire list of un-confirmed transactions.
* `Mine block` - This does verification of transactions to be added to a block.
* `Verify blockchain` - This verifies the entire blockchain structure.
* `Generate RSA keys` - New RSA keys for the manufacturer and stakeholders can be created.
* `Track an item` - This allows to track a particular item through the blockchain.

# Screenshots
<p align="center"> <img src = 'images/step1.png' </p>
<p align="center"> <img src = 'images/step2.png' </p>
<p align="center"> <img src = 'images/step3.png' </p>
<p align="center"> <img src = 'images/step4.png' </p>
<p align="center"> <img src = 'images/step5.png' </p>
<p align="center"> <img src = 'images/step6.png' </p>
