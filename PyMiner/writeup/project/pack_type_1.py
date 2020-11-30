import sys

file = sys.argv[1]

result = """
def KSA(key):
    keylength = len(key)
    S = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]  # swap
    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap
        K = S[(S[i] + S[j]) % 256]
        yield K


def RC4(key):
    S = KSA(key)
    return PRGA(S)


import string
import struct
import base64
ok = False
key = 0
cipher = base64.b64decode({})
while not ok:
    k = struct.pack(">I", key)
    keystream = RC4(k)
    plain = [cipher[i]^next(keystream) for i in range(len(cipher))]
    if any(chr(i) not in string.printable for i in plain):
        key+=1
        continue
    exec("".join(chr(i) for i in plain))
    break
# """

def KSA(key):
    keylength = len(key)
    S = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]  # swap
    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap
        K = S[(S[i] + S[j]) % 256]
        yield K


def RC4(key):
    S = KSA(key)
    return PRGA(S)

key = bytearray(b"\x00\x00\x0c\xa7")
f = open(file, "rb").read()
keystream = RC4(key)
import base64
cip = bytes([f[i]^next(keystream) for i in range(len(f))])

keystream2 = RC4(key)
dec = bytes([cip[i]^next(keystream2) for i in range(len(cip))])
print(dec)

open(sys.argv[1]+".m1", "w").write(result.format(base64.b64encode(cip)))