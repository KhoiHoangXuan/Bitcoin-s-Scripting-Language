from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2shAddress
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
    with open("multisig_info.txt", "w") as file:
        file.write(f"Private Key 1: {private_key1.to_wif()}\n")
        file.write(f"Private Key 2: {private_key2.to_wif()}\n")
        file.write(f"Public Key 1: {public_key1.to_hex()}\n")
        file.write(f"Public Key 2: {public_key2.to_hex()}\n")
        file.write(f"Redeem Script: {redeem_script.to_hex()}\n")
        file.write(f"P2SH Address: {address.to_string()}\n")

def callAPI(address):
    url = f'https://blockstream.info/testnet/api/address/{address}/txs'
    response = requests.get(url)

    # Kiểm tra phản hồi từ API
    if response.status_code == 200:
        # Chuyển đổi dữ liệu từ JSON
        transactions = response.json()
        
        # In ra thông tin giao dịch
        if transactions:
            print(f"Transactions for address {address}:")
            tx = transactions[0]['vin']
            print('hahhqahahhaha\n', tx, '\nahahaha')
            txid = tx[0]['txid']
            # version = tx['version']
            # locktime = tx['locktime']
            # vin = tx['vin']
            vout = tx[0]['vout']
            # is_coinbase = tx['is_coinbase']
            # fee = tx['fee']
            # print(f"\nTransaction ID: {txid}")
            # print(f"Version: {version}")
            # print(f"Locktime: {locktime}")
            # print(f"Is Coinbase: {is_coinbase}")
            # print(f"Fee: {fee} satoshis")
            
            # # In thông tin inputs (vin)
            # print("Inputs (vin):")
            # for input_tx in vin:
            #     prev_txid = input_tx['txid']
            #     prev_vout = input_tx['vout']
            #     prev_address = input_tx['prevout']['scriptpubkey_address']
            #     value = input_tx['prevout']['value']
            #     print(f"  TXID: {prev_txid}, Vout: {prev_vout}, Address: {prev_address}, Value: {value} satoshis")
            
            # # In thông tin outputs (vout)
            # print("Outputs (vout):")
            # for output_tx in vout:
            #     output_address = output_tx['scriptpubkey_address']
            #     output_value = output_tx['value']
            #     print(f"  Address: {output_address}, Value: {output_value} satoshis")
        else:
            print("No transactions found for this address.")
    else:
        print(f"Error: {response.status_code}")
    return txid, vout

def spend_multisig():
    with open("list.txt", "r") as file:
        lines = file.readlines()
        # Lấy các private key từ tệp
        private_key1f = lines[0].strip().split(": ")[1]  # Dòng đầu tiên là Private Key 1
        private_key2f = lines[1].strip().split(": ")[1]  # Dòng thứ hai là Private Key 2

    # Khóa riêng
    private_key1 = PrivateKey(private_key1f)
    private_key2 = PrivateKey(private_key2f)

    # Khóa công khai
    public_key1 = private_key1.get_public_key().to_hex()
    public_key2 = private_key2.get_public_key().to_hex()

    # Tạo 2-of-2 multisig script
    redeem_script = Script(['OP_2', public_key1, public_key2, 'OP_2', 'OP_CHECKMULTISIG'])
    address = P2shAddress.from_script(redeem_script)
    print("P2SH Address:", address.to_string())

    txid, vout = callAPI('2Msv6A25gy1p4EAGfMDjFj34bXqspmPavRk')
    print(txid)
    print(vout)

    # Tạo transaction input
    txin = TxInput(txid, vout)



def main():
    # private_key1, private_key2, public_key1, public_key2, redeem_script, address = setup_multisig()
    # # In kết quả
    # print("Private Key 1:", private_key1.to_wif())
    # print("Private Key 2:", private_key2.to_wif())
    # print("Public Key 1:", public_key1)
    # print("Public Key 2:", public_key2)
    # print("Redeem Script:", redeem_script.to_hex())
    # print("P2SH Address:", address.to_string())
    spend_multisig()
    print('haha')

main()
