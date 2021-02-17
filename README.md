# Introduction

Using this code and the required dependencies, we will be using a single mnemonic and its corresponding master key in order to transact using a few different cryptocurrency types, namely *Bitcoin* and *Ethereum*. To do this, we will be using a universal, multi-coin wallet with BIP44 standard that allows us to generate multiple addresses associated with different cryptocurrencies (i.e. Bitcoin, Ethereum, Dodge Coin, ect.). This standard is much like the BIP32, hierarchical derivation standard that allows users to derive a tree of address from a root key. However, the BIP44 standard takes it a step further and allows you to derive multiple trees for multiple cryptocurrencies, which we will need for the purposes of conducting commerce in multiple different monetary (albeit digital) modes. 

# Deriving and Storing the Bitcoin and Ethereum Address

In order to perform transactions later one, we will need to first use our derive symlink (please reference the **requirements** file for more information) in order to pull in the address, public and private keys for both Ethereum and Bitcoin. We can put the derive command into a function were we will pass it our mnemonic and coin type in order to retrieve the address. 

[derive_function](Images/Derive_Function.png)

Since we have stored the output in a .json format, we will be able to easily put the results for both Ethereum and Bitcoin into a dictionary object. This will allow us to easily pull out different private and public keys, as well as address, to help facilitate transactions later. 

[coins](Images/coin_object.png)

# Sending Transactions

After creating that coins object to store our wallet information, we are reading to being transacting between the two. Before we do that, however, we will need to set up a few functions to help us facilitate the flow of funds between wallet address.

## Functions

1) The first function we will need will be called `priv_key_to_account` and will allow us to take a private key string in a child key, that being what is in our coin object above, and convert it to an account object that `bit` or `web3.py` can use to transact.

[private_key_to_account](Images/private_key_to_account.png)

Later, we will call this to identify the address we need to add to our ethereum network .json and to send a transaction using bitcoin. 

2) The next function is called `create_tx` and will create the raw, unsigned transaction that contains all metadata needed to transact. 

[create_tx](Images/create_tx.png)

We will be using this function in the next most immediate function.

3) The third and final function that we will be creating is called `send_tx`, which will call the `create_tx` function in order to sign the transaction, then send it to the designated network.

[send_tx](Images/send_tx.png)

After defining our functions above we can then call each of them in order to facilitate transactions between addresses using both Bitcoin and Ethereum. 

## Bitcoin Transactions

In order to send transactions using the code in the wallet.py file, we first need to fund our wallets. To fund our Bitcoin wallet we will need to:

1) Open up Terminal and cd into the wallet folder

2) Using https://bitcoinfaucet.uo1.net/send.php link, fund one of the bitcoin addresses. You can use the coin object that we previously created in order to pull out an address that you would like to fund. For the purposes of this code, I just simple used the first address. After running some Python code to derive the funding address you can feed it into the faucet link to get testnet Bitcoin. 

[funding_address](Images/funding_address.png)

[faucet](Images/Funding_BTC)

[faucet_confirmation](Images/Funding_confirmation.png)

3) After funding one of our wallet address we will then have to define which address will be our sender and which will be our receiver. For the sending account we will need the private key and for the recipient we will only need the address. We can derive both of these by referencing our coin object above.

[sending_and_receiving](Images/send_and_receive.png)

4) After deriving the two addresses and their role in our upcoming transaction we can set up the transaction code. We will be calling our **send_tx** function in order to do so. We will also have to call our **priv_key_to_account** in order to derive the account object that bit will need to interact with our sending wallet.

[transaction_setup](Images/transaction_setup.png)

5) After setting this code up in our Python file, we can run it in our Terminal window, provided that we are still cd into the proper folder and our ethereum network is activated. In order to run the code in Terminal we can executed **python multi_wallet.py** command in the Terminal window. 

[terminal_command](Images/terminal_command.png)

6) While the balances in our terminal window above look unchanged that is because it takes sometime for the transaction to be confirmed on the Bitcoin Testnet. We can use [block explorer](https://tbtc.bitaps.com/) in order to keep track of the progress of our transaction. 

[transaction_unconfirmed](Images/Unconfirmed.png)

[transaction_confirmed](Images/Confirmed.png)

## Ethereum Transactions

There are a few steps that we need to completed in order to transact using our Ethereum Proof of Authority network that is already in existence:

1) Using the coins object that we created previous, pull out an address for one of our ethereum wallets. 

[eth_address](Images/eth_address.png)

2) Add this address to the POA Ethereum network .json file.

[add_to_json](Images/adding_to_json.png)

3) Delete the geth folders in node 1 and node 2.

4) Re-initialize using `geth --datadir nodeX init networkname.json`. This will create a new chain, and will pre-fund the new account.

[initialize_network](Images/initialize_network.png)

5) After re-initializing the network, we then need to begin the mining process in order to get the network running. 

[mining_node1](Images/node_1.png)

[mining_node2](Images/node_2.png)



