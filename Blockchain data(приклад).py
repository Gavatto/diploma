from web3 import Web3
import json
import random
from datetime import datetime

# Підключення до Ethereum
w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

# Доступ до смарт-контракту
contract_address = '0xYourContractAddress'
abi = json.loads('[ABI of the contract]')
contract = w3.eth.contract(address=contract_address, abi=abi)

# Власний гаманець
wallet_address = '0xYourWalletAddress'
private_key = 'YourPrivateKey'

def record_energy_data(panel_id):
    produced_energy = round(random.uniform(1.5, 3.5), 2)
    consumed_energy = round(random.uniform(1.0, 2.0), 2)
    timestamp = int(datetime.now().timestamp())

    # Підготовка транзакції
    txn = contract.functions.recordEnergyData(
        int(produced_energy * 1000),  # У кВт
        int(consumed_energy * 1000),  # У кВт
        timestamp,
        panel_id
    ).buildTransaction({
        'chainId': 4,  # Rinkeby testnet chain ID
        'gas': 200000,
        'gasPrice': w3.toWei('10', 'gwei'),
        'nonce': w3.eth.getTransactionCount(wallet_address),
    })

    # Підписання та відправка транзакції
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Очікування підтвердження
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return tx_receipt

# Приклад запису даних
panel_id = 'SP-001'
receipt = record_energy_data(panel_id)
print(f"Транзакція підтверджена: {receipt.transactionHash.hex()}")
