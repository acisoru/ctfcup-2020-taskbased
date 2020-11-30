#!/usr/bin/env python3.7

import json

from flask import Flask, request, render_template
from string import hexdigits
from libcrypt import AES128, CipherMode
from waitress import serve


app = Flask(__name__)


@app.route('/')
def handle_index():
    return render_template('index.html')


def make_error(text):
    return json.dumps({
        'iv': None,
        'result': text
    })


@app.route('/encrypt', methods=['POST'])
def handle_encrypt():
    if not request.is_json:
        return make_error('please json'), 400

    key = request.json.get('key')
    if key is None:
        return make_error('key is none'), 400

    mode = request.json.get('mode')
    if mode is None:
        return make_error('mode is none'), 400

    plaintext = request.json.get('plaintext')
    if plaintext is None:
        return make_error('plaintext is none'), 400

    if any(symbol not in hexdigits for symbol in key) or len(key) != AES128.BLOCK_SIZE * 2:
        return make_error('invalid key'), 400
    
    try:
        mode = CipherMode[mode.upper()]
    except Exception:
        return make_error('invalid mode'), 400

    aes = AES128(key, mode)
    iv, result = aes.encrypt(plaintext.encode())
    return json.dumps({
        'iv': iv,
        'result': result
    })


@app.route('/decrypt', methods=['POST'])
def handle_decrypt():
    if not request.is_json:
        return make_error('please json'), 400

    iv = request.json.get('iv')

    key = request.json.get('key')
    if key is None:
        return make_error('key is none'), 400

    mode = request.json.get('mode')
    if mode is None:
        return make_error('mode is none'), 400

    ciphertext = request.json.get('ciphertext')
    if ciphertext is None:
        return make_error('ciphertext is none'), 400

    if len(key) != AES128.BLOCK_SIZE * 2:
        return make_error('invalid key'), 400

    if any(symbol not in hexdigits for symbol in ciphertext):
        return make_error('invalid ciphertext'), 400
    
    try:
        mode = CipherMode[mode.upper()]
    except Exception:
        return make_error('invalid mode'), 400

    aes = AES128(key, mode)
    result = aes.decrypt(bytes.fromhex(ciphertext), iv)
    return json.dumps({
        'result': result
    })


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=31337)
