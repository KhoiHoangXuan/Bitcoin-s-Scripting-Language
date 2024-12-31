from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2pkhAddress
import os

# Thiết lập môi trường testnet
setup('testnet')

# Tạo private key ngẫu nhiên
private_key = PrivateKey()

# Lấy public key từ private key
public_key = private_key.get_public_key()

# Tạo địa chỉ Bitcoin (P2PKH) từ public key
address = public_key.get_address()

# Ghi file
with open("list.txt", "a") as file:
    file.write(f"\nPrivate Key recipient: {private_key.to_wif()}\n")
    file.write(f"Public Key recipient: {public_key.to_hex()}\n")
    file.write(f"Address recipient: {address.to_string()}\n")
