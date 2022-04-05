from flask import Flask, jsonify, request, json
from uuid import uuid4
from time import time
import hashlib, json

#FLASK APP
app = Flask('__name__')

#BLOCKCHAIN
nodes = set()
current_transactions = []
chains = []

#CREATE NEW BLOCK
def create_block(txs, last_hash, proof, node_id, lngth):
    block = {
        'index': lngth,
        'time': time(),
        'transactions': txs,
        'proof': proof,
        'previous_hash': last_hash
    }
    for c in chains:
        if node_id == c['id']:
            c['chain'].append(block)
    return block

#DEMO INTERACTION
@app.route('/chain', methods=['POST'])
def get_chain():
    data = request.get_json()
    for c in chains:
        if data == c['id']:
            return jsonify(c['chain']), 200
        else:
            continue
    
@app.route('/register', methods=['POST'])
def register_node():
    data = request.get_json()
    #NODE ID
    node_id = str(uuid4()).replace('-', '')
    #ADD NODE
    nodes.add(node_id)
    #CREATE CHAIN
    chains.append({'chain': [], 'TX': [], 'id': node_id})
    #GENESIS BLOCK
    create_block([{'sender': 'Selena', 'receiver': node_id, 'amount': 1}], 100, 1, node_id, 0);

    return jsonify(node_id), 200

@app.route('/prev-block', methods=['POST'])
def get_prev_block():
    data = request.get_json()
    for c in chains:
        if data == c['id']:
            return jsonify(c['chain'][-1]), 200
        else:
            continue

@app.route('/hash-block', methods=['POST'])
def hash_block_string():
    data = request.get_json()
    block_string = json.dumps(data, sort_keys=True).encode()
    hash = hashlib.sha256(block_string).hexdigest()
    return jsonify(hash), 200
    
@app.route('/valid_proof', methods=['POST'])
def valid_proof():
    data = request.get_json()
    attempt = f'{data["last_proof"]}{data["proof"]}{data["last_hash"]}'.encode()
    attempt = hashlib.sha256(attempt).hexdigest()
    return jsonify(attempt), 200

@app.route('/transaction', methods=['POST'])
def new_transaction():
    data = request.get_json()
    for c in chains:
        if data == c['id']:
            sender = 'Selena'
            recipient = data
            amount = 1
            tx = {'sender': sender, 'recipient': recipient, 'amount': 1}
            c['TX'].append(tx)
            return jsonify(c['TX'][-1]), 200
        else:
            continue

@app.route('/new', methods=['POST'])
def newBlock():
    data = request.get_json()
    block_string = json.dumps(data[0], sort_keys=True).encode()
    last_hash = hashlib.sha256(block_string).hexdigest()
    proof = data[1]
    for c in chains:
        if data[2] == c['id']:
            lngth = len(c['chain'])
            txs = c['TX']
            return jsonify(create_block(txs, last_hash, proof, data[2], lngth)), 200

#APP
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=process.ENV.PORT || 9002)