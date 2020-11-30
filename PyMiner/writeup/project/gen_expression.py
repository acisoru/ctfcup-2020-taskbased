import sys, random

flag = sys.argv[1]
assert flag.startswith("ctfcup{") and flag.endswith("}") # из условия таска


flag = list(flag)
pos = [i for i in range(len(flag))]
exp = [] # pos1, pos2, f[pos1]-f[pos2]

# часть флага уже известна - ctfcup{...}
#                            0123456   -1
# уравнение без каких-либо известных элементов, придется перебирать в системе
#  элемент без пары
for i in [len(flag)-1, 6, 5, 4, 3, 2, 1, 0]:
    pos.pop(i)



while pos:
    pos1 = random.choice(pos)
    pos.remove(pos1)

    if pos:
        pos2 = random.choice(pos)
    else:
        break
    #pos.remove(pos2)

    exp.append((pos1, pos2,
                ord(flag[pos1]) - ord(flag[pos2])
                ))

blueprint = "flag[{}] - flag[{}] == {}"
blueprint2 = "flag[{}] == {}"

ans = []
for i in exp:
    if i[1] is None:
        continue
        #ans.append(blueprint2.format(i[0], i[2]))
    else:
        ans.append(blueprint.format(i[0], i[1], i[2]))
print(" and ".join(ans))


### доказательство решаемости
import z3
for i in range(256):
    s = z3.Solver()
    a = z3.IntVector("a", len(flag))
    for _ in a:
        s.add(_ >= 0x20)
        s.add(_ <= 0x7E)
    for e in exp:
        s.add(a[e[0]] - a[e[1]] == e[2])
    s.add(a[7] == i)
    if s.check() == z3.sat:
        m = s.model()
        print("".join(chr(m[q].as_long()) for q in a))

"""
       W SS#]NB"2a"CNAh?b6Z&@EQR
       X!TT$^OC#3b#DOBi@c7['AFRS
       Y"UU%_PD$4c$EPCjAd8\(BGST
       Z#VV&`QE%5d%FQDkBe9])CHTU
       [$WW'aRF&6e&GRElCf:^*DIUV
       \%XX(bSG'7f'HSFmDg;_+EJVW
       ]&YY)cTH(8g(ITGnEh<`,FKWX
       ^'ZZ*dUI)9h)JUHoFi=a-GLXY
       _([[+eVJ*:i*KVIpGj>b.HMYZ
       `)\\,fWK+;j+LWJqHk?c/INZ[
       a*]]-gXL,<k,MXKrIl@d0JO[\
       b+^^.hYM-=l-NYLsJmAe1KP\]
       c,__/iZN.>m.OZMtKnBf2LQ]^
       d-``0j[O/?n/P[NuLoCg3MR^_
       e.aa1k\P0@o0Q\OvMpDh4NS_`
       f/bb2l]Q1Ap1R]PwNqEi5OT`a
       g0cc3m^R2Bq2S^QxOrFj6PUab
       h1dd4n_S3Cr3T_RyPsGk7QVbc <- !!!
       i2ee5o`T4Ds4U`SzQtHl8RWcd
       j3ff6paU5Et5VaT{RuIm9SXde
       k4gg7qbV6Fu6WbU|SvJn:TYef
       l5hh8rcW7Gv7XcV}TwKo;UZfg
       m6ii9sdX8Hw8YdW~UxLp<V[gh
"""