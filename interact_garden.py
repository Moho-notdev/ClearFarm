from web3 import Web3
import json, os

# Config
RPC = os.getenv("AVAX_RPC", "https://api.avax-test.network/ext/bc/C/rpc")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")  # dopo il deploy
CHAIN_ID = 43113  # Fuji

w3 = Web3(Web3.HTTPProvider(RPC))
assert w3.isConnected(), "Non connesso all'RPC"

# Carica ABI
with open("out/Garden.sol/Garden.json") as f:
    artifact = json.load(f)
ABI = artifact["abi"]

contract = w3.eth.contract(address=Web3.toChecksumAddress(CONTRACT_ADDRESS), abi=ABI)

# Funzioni utili
def plant_plot(species, organic_cert, token_uri):
    acct = w3.eth.account.from_key(PRIVATE_KEY)
    tx = contract.functions.plantPlot(species, organic_cert, token_uri).buildTransaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 300000,
        "gasPrice": w3.eth.gas_price,
        "chainId": CHAIN_ID,
    })
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("Tx sent:", tx_hash.hex())
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Receipt:", receipt)
    return receipt

def water_plot(plot_id, amount):
    acct = w3.eth.account.from_key(PRIVATE_KEY)
    tx = contract.functions.waterPlot(plot_id, amount).buildTransaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 200000,
        "gasPrice": w3.eth.gas_price,
        "chainId": CHAIN_ID,
    })
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Watered plot", plot_id, "Tx:", tx_hash.hex())
    return receipt

def get_plot(plot_id):
    return contract.functions.getPlot(plot_id).call()
