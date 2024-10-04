from web3 import Web3
import json
import random
import time
from datetime import datetime
from dotenv import load_dotenv
import os

# Завантаження .env файлу для конфіденційних даних
load_dotenv()

# Підключення до Infura
infura_url = os.getenv("INFURA_URL")
w3 = Web3(Web3.HTTPProvider(infura_url))

# Адреса контракту і ABI
contract_address = os.getenv("CONTRACT_ADDRESS")
with open('solar_energy_monitor/abi/SolarEnergyMonitorABI.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

# Підключення до контракту
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Адреса гаманця та приватний ключ
wallet_address = os.getenv("WALLET_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Функція для запису енергетичних даних
def record_energy_data(panel_id, produced_energy, consumed_energy):
    timestamp = int(datetime.now().timestamp())
    
    # Створення транзакції
    transaction = contract.functions.recordEnergyData(
        produced_energy, 
        consumed_energy, 
        timestamp, 
        panel_id
    ).buildTransaction({
        'chainId': 4,  # Rinkeby
        'gas': 200000,
        'gasPrice': w3.toWei('10', 'gwei'),
        'nonce': w3.eth.getTransactionCount(wallet_address),
    })

    # Підписання транзакції
    signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)

    # Відправка транзакції
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    
    # Очікування підтвердження
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Транзакція підтверджена: {tx_receipt.transactionHash.hex()}")

# Генерація тестових даних та запис
for i in range(5):
    panel_id = 'SP-001'
    produced_energy = random.randint(1500, 3500)  # В кВт
    consumed_energy = random.randint(1000, 2000)  # В кВт
    record_energy_data(panel_id, produced_energy, consumed_energy)
    time.sleep(2)  # Затримка між записами
