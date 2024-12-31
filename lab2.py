from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2shAddress
from bitcoinutils.script import Script

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
    return private_key1, private_key2, public_key1, public_key2, redeem_script, address

def main():
    # private_key1, private_key2, public_key1, public_key2, redeem_script, address = setup_multisig()
    # # In kết quả
    # print("Private Key 1:", private_key1.to_wif())
    # print("Private Key 2:", private_key2.to_wif())
    # print("Public Key 1:", public_key1)
    # print("Public Key 2:", public_key2)
    # print("Redeem Script:", redeem_script.to_hex())
    # print("P2SH Address:", address.to_string())

    print('haha')

main()
