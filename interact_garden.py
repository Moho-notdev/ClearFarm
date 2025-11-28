from web3 import Web3
import json, os

# Config
RPC = os.getenv("AVAX_RPC", "https://api.avax-test.network/ext/bc/C/rpc")  # Fuji Testnet
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

# Funzione generica per inviare transazioni con gas ottimizzato
def send_tx(function_call):
    acct = w3.eth.account.from_key(PRIVATE_KEY)
    tx = function_call.build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 300000,
        "gasPrice": w3.to_wei(2, "gwei"),  # Gas price ridotto
        "chainId": CHAIN_ID,
    })
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("Tx inviata:", tx_hash.hex())
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Receipt:", receipt)
    return receipt

# Funzioni specifiche
def plant_plot(species, organic_cert, token_uri):
    return send_tx(contract.functions.plantPlot(species, organic_cert, token_uri))

def water_plot(plot_id, amount):
    return send_tx(contract.functions.waterPlot(plot_id, amount))

def get_plot(plot_id):
    return contract.functions.getPlot(plot_id).call()
