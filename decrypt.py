#!/usr/bin/env python3

import pem
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import sys
import os

def load_private_key(file_path):
    parsed = pem.parse_file(file_path)
    return parsed[0]


DATA = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDOgNbRgXgVEwYIIws0O7I/jczfQ/pgBYZ/kNuI3rzWhU+Ucnkf
Mu9iel5swcgEsxiGG/uKa2A4mSiBrswsQwQzzIfILRxpk3EnPpS/OYhpfRJwiuDr
rC6WPrxwVbIzLFOcGZP5/xoU5Evgaq2jmcHNDcEVvaIrTzFFHblC50VJbwIDAQAB
AoGAI44jbqcwGdDQtQ3zm+a7Zh3wLHDz5xyMb+JtKj/Pm9AQR6r+F9UZSodvQqKK
4eREULL4uHiMdLJKOynxlZ1kV4etE8U/5aIxa6m+SKwLZSkDz8jTS2GV5Ki0DxKC
BCHAqb70lu3xQ2DOl4Uim/r5DQieB4L/hpmkYHLp2CK1J4ECQQDov5gwGDdR3cdu
iurpv6iKHRqW7b9CGyUApWZzd3jgbBkcdG5PgGFIklgNQLhZhHjCGVI2HRH+sTOp
hcRMOzM/AkEA4yIKXaum0eLrCftvtciLfTx2yguUe3h8Esl0RdiRvMbakbckie+E
6ri1YdLk9BQhKqTymrCH6OOpeQytDlnN0QJBALMeX/0DZe93AngsKMVjXk2MQF5O
8ZXqVfu9Tq8mDryH9HtVj19XqYa0OVdZq4YY0OZvnjlO/f5IWT3pWDxigvkCQQCZ
x+5kxVdJO+4O8CIOXh2zSUDUQ0rg3g6DWcpTj/H8claB2hHvIjBIC48jEHrbltVt
3gg0G9mpIJsZzi9NTBhBAkAVZNd7iLAJgB+izG7gmcpKWwhj2hAH7xZgu3eWqCqG
Q/ZMDGZ1Asg237g6oOz85t7MHGrcIR6ezER2rz/7BMW0
-----END RSA PRIVATE KEY-----
"""

def private_key_from_string():
    return PKCS1_OAEP.new(RSA.importKey(DATA.encode()), hashAlgo=SHA256)


def private_key_from_file(file_path):
    with open(file_path, "rb") as key_data:
        return PKCS1_OAEP.new(RSA.importKey(key_data.read()), hashAlgo=SHA256)

def decrypt_file(file_path, k):
    with open(file_path, mode="rb") as infile, open(os.path.basename(file_path) + "_decrypted2", "wb") as out:
        d =  infile.read()
        for line in d.split(b"block:"):
            if len(line) == 0 :
                continue
            out.write(decrypt_msg_in_chunks(line, k))


def decrypt_msg_in_chunks(msg, key_data):
    msg_size = len(msg)
    step = 128
    out = [key_data.decrypt(msg[start:min(start + step,msg_size)]) for start in range(0, msg_size, step)]
    return b''.join(out)
    
    """
    for start in range(0, msg_size, step):
        finish = start + step
        if finish > msg_size:
            finish = msg_size
        decryptedBlocks = key_data.decrypt(msg[start:finish])
        wf.write(decryptedBlocks)
        wf.flush()
        res += decryptedBlocks
    wf.close()
    return res

====================================

    msg_size = len(msg)
    step = 128
    
    res = b''

    for start in range(0, msg_size, step):
        finish = start + step
        if finish > msg_size:
            finish = msg_size
        decryptedBlocks = key_data.decrypt(msg[start:finish])
        res += decryptedBlocks

    return res
"""
    
def rsa_decrypt(message, priv_key):
    '''
    rsa decrypt
    :param ciphertext:ciphertext
    :param priv_key:Private key
    '''
    length = len(message)
    default_length = 128
    if length <= default_length:
        return priv_key.decrypt(message)
    # Need segmentation
    offset = 0
    result = []
    while length - offset > 0:
        if length - offset > default_length:
            result.append(priv_key.decrypt(message[offset:offset+default_length]))
        else:
            result.append(priv_key.decrypt(message[offset:]))
        offset += default_length
    decode_message = [x.decode("utf-8") for x in result]
    return "".join(decode_message)



if __name__ == "__main__":
    key = private_key_from_string()
    decrypt_file(sys.argv[1], key)
