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


def callAPI(address):
    url = f'https://blockstream.info/testnet/api/address/{address}/utxo'
    print(url)
    response = requests.get(url)

    # Kiểm tra phản hồi từ API
    if response.status_code == 200:
        # Chuyển đổi dữ liệu từ JSON
        utxo = response.json()
        
        # Lấy thông tin UTXO
        if utxo:
            tx = utxo[0]
            txid = tx['txid']
            vout = tx['vout']
            value = tx['value']
            return txid, vout, value
        else:
            print("No UTXO found for this address.")
    else:
        print(f"Error: {response.status_code}")


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

    # Địa chỉ multisig
    multisig_address = P2shAddress.from_script(redeem_script)


    txid, vout, value = callAPI(multisig_address.to_string())


    # Tạo transaction input
    txin = TxInput(txid, vout)

    # Các thông tin của transaction output
    amount_to_send = 700
    destination_address = P2pkhAddress(destination_address).to_script_pub_key()
    fee = 9800

    # Tạo transaction output
    txout = TxOutput(amount_to_send, destination_address)
    
    
    
    # Tạo transaction output để chuyển lại tiền thừa cho địa chỉ multisig
    changes = value - amount_to_send - fee
    txout_changes = TxOutput(changes, multisig_address.to_script_pub_key())


    tx = Transaction([txin], [txout])
    # Sign the transaction with the first private key
    sig1 = private_key1.sign_input(tx, 0, redeem_script)

    # Sign the transaction with the second private key
    sig2 = private_key2.sign_input(tx, 0, redeem_script)

    # Step 7: Create the scriptSig (including both signatures and the redeem script)
    script_sig = Script(['OP_0', sig1, sig2, redeem_script.to_hex()])
    # script_sig = Script([sig1, sig2])
    tx.inputs[0].script_sig = script_sig
    signed_tx = tx.serialize()
    broadcast_transaction(signed_tx)







def main():
    spend_multisig()

main()
