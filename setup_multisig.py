from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2shAddress, P2pkhAddress
from bitcoinutils.script import Script
import requests
from bitcoinutils.transactions import Transaction, TxInput, TxOutput

def setup_multisig():
    # Thiết lập môi trường cho Testnet
    setup('testnet')

    # Tạo hai khóa riêng ngẫu nhiên
    private_key1 = PrivateKey()
    private_key2 = PrivateKey()

    # Lấy khóa công khai tương ứng
    public_key1 = private_key1.get_public_key().to_hex()
    public_key2 = private_key2.get_public_key().to_hex()

    # Tạo 2-of-2 multisig script
    redeem_script = Script(['OP_2', public_key1, public_key2, 'OP_2', 'OP_CHECKMULTISIG'])

    # Tạo địa chỉ P2SH từ redeem script
    address = P2shAddress.from_script(redeem_script)

    # Ghi file
    with open("list.txt", "w") as file:
        # In ra màn hình
        print(f"Private Key 1: {private_key1.to_wif()}")
        print(f"Private Key 2: {private_key2.to_wif()}")
        print(f"Public Key 1: {public_key1}")
        print(f"Public Key 2: {public_key2}")
        print(f"Redeem Script: {redeem_script.to_hex()}")
        print(f"P2SH Address: {address.to_string()}")
        # Ghi file
        file.write(f"Private Key 1: {private_key1.to_wif()}\n")
        file.write(f"Private Key 2: {private_key2.to_wif()}\n")
        file.write(f"Public Key 1: {public_key1}\n")
        file.write(f"Public Key 2: {public_key2}\n")
        file.write(f"Redeem Script: {redeem_script.to_hex()}\n")
        file.write(f"P2SH Address: {address.to_string()}")

setup_multisig()