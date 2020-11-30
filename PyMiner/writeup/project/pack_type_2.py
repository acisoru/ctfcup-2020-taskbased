import sys

file = sys.argv[1]

result = """\
import string, zlib
print("meow")
key = 0
c = zlib.decompress({})
while 1:
 p = [c[i]^key for i in range(len(c))]
 try:
  exec("".join(chr(i) for i in p))
  break
 except:
  key+=1
"""

import random
import zlib
rounds = 24
f = open(file, "rb").read()
for i in range(rounds):
    print(i, len(f))
    #key = random.randrange(0, 40-i)
    key = random.randrange(0, rounds-i)
    cip = bytes([f[i] ^ key for i in range(len(f))])
    f = result.format(zlib.compress(cip)).encode()
    open("ana.py", "wb").write(f)


#open(sys.argv[1] + ".m2", "w").write(result.format(base64.b64encode(cip)))