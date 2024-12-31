from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2pkhAddress
import os

# Thiết lập môi trường testnet
setup('testnet')

# Tạo private key ngẫu nhiên
private_key = PrivateKey(secret=os.urandom(32))

# Lấy public key từ private key
public_key = private_key.get_public_key()

# Tạo địa chỉ Bitcoin (P2PKH) từ public key
address = P2pkhAddress(public_key.get_address())

