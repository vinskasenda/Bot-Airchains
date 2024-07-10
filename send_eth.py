import random
import time
from web3 import Web3
from eth_account import Account

def random_address():
    """Generate a random EVM address."""
    return Account.create().address

def send_eth(private_key, to_address, amount_eth, rpc_url, chain_id):
    """Send ETH from one address to another."""
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if not web3.is_connected():
        print("Failed to connect to the RPC URL")
        return
    
    account = Account.from_key(private_key)
    
    while True:
        try:
            # Fetch the latest nonce dynamically
            nonce = web3.eth.get_transaction_count(account.address, 'pending')
            
            # Create the transaction
            tx = {
                'nonce': nonce,
                'to': to_address,
                'value': web3.to_wei(amount_eth, 'ether'),
                'gas': 2000000,
                'gasPrice': web3.to_wei('5', 'gwei'),
                'chainId': chain_id
            }

            # Sign the transaction
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)

            # Send the transaction
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'Transaction sent with hash: {web3.to_hex(tx_hash)} to address {to_address}')
            break  # Exit the loop if transaction succeeds

        except ValueError as e:
            print(f"Error occurred: {e}")
            print("Retrying...")
            time.sleep(1)  # Wait for 1 second before retrying

if __name__ == "__main__":
    # Provided private key
    PRIVATE_KEY = 'YOUR PRIVATE KEY' #Fill with your Private Key
    RPC_URL = 'YOUR RPC URL' # Fill with your RPC
    CHAIN_ID = 1234
    AMOUNT_ETH = 0.1  # Amount of ETH to send

    try:
        while True:
            random_to_address = random_address()
            send_eth(PRIVATE_KEY, random_to_address, AMOUNT_ETH, RPC_URL, CHAIN_ID)  # Send ETH to the random address
            time.sleep(1)  # Add a delay of 1 second between transactions to avoid spamming
    except KeyboardInterrupt:
        print("Script interrupted by user. Exiting...")
