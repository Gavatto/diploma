from web3 import Web3
import json
from solcx import compile_standard

# Завантаження контракту з файлу
with open('solar_energy_monitor/contracts/SolarEnergyMonitor.sol', 'r') as file:
    contract_source_code = file.read()

# Компіляція контракту
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"SolarEnergyMonitor.sol": {"content": contract_source_code}},
    "settings": {
        "outputSelection": {
            "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
        }
    }
})

# Отримання bytecode та ABI
bytecode = compiled_sol['contracts']['SolarEnergyMonitor.sol']['SolarEnergyMonitor']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['SolarEnergyMonitor.sol']['SolarEnergyMonitor']['abi']

# Підключення до мережі через Infura
w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID'))

# Адреса гаманця
wallet_address = '0xYourWalletAddress'
private_key = 'YourPrivateKey'

# Створення контракту
SolarEnergyMonitor = w3.eth.contract(abi=abi, bytecode=bytecode)

# Підготовка транзакції для деплойменту контракту
nonce = w3.eth.getTransactionCount(wallet_address)
transaction = SolarEnergyMonitor.constructor().buildTransaction({
    'chainId': 4,
    'gas': 2000000,
    'gasPrice': w3.toWei('20', 'gwei'),
    'nonce': nonce
})

# Підписання транзакції приватним ключем
signed_txn = w3.eth.account.signTransaction(transaction, private_key=private_key)

# Відправка транзакції
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(f"Транзакція на деплой контракту відправлена: {txn_hash.hex()}")

# Очікування підтвердження
txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
print(f"Контракт задеплоєний за адресою: {txn_receipt.contractAddress}")

# Зберігаємо ABI у файл
with open('solar_energy_monitor/abi/SolarEnergyMonitorABI.json', 'w') as abi_file:
    json.dump(abi, abi_file)
