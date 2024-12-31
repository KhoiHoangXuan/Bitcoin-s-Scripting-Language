from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2shAddress, P2pkhAddress
from bitcoinutils.script import Script
import requests
from bitcoinutils.transactions import Transaction, TxInput, TxOutput

def broadcast_transaction(tx_hex):
    url = "https://mempool.space/testnet/api/tx"
    headers = {"Content-Type": "text/plain"}

    try:
        response = requests.post(url, data=tx_hex, headers=headers)
        print(f"Phản hồi từ server: {response.status_code}, {response.text}")
        
        if response.status_code == 200:  # Thành công
            print("Broadcast successfully!")
            print("Transaction ID (txid):", response.text.strip())
        else:
            print(f"Broadcast failed: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
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
        destination_address = lines[8].strip().split(": ")[1]
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
    amount_to_send = 2000
    destination_address = P2pkhAddress(destination_address).to_script_pub_key()


    txout = TxOutput(amount_to_send, destination_address)
    # print(destination_address)
    tx = Transaction([txin], [txout])
    # Sign the transaction with the first private key
    sig1 = private_key1.sign_input(tx, 0, redeem_script)

    # Sign the transaction with the second private key
    sig2 = private_key2.sign_input(tx, 0, redeem_script)

    # Step 7: Create the scriptSig (including both signatures and the redeem script)
    script_sig = Script([sig1, sig2])
    tx.inputs[0].script_sig = script_sig
    signed_tx = tx.serialize()
    broadcast_transaction(signed_tx)







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
