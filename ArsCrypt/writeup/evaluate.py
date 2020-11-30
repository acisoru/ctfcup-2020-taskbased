import bitmap_work

def block(code):
    opened = []
    blocks = {}
    for i in range(len(code)):
        if code[i] == '[':
            opened.append(i)
        elif code[i] == ']':
            blocks[i] = opened[-1]
            blocks[opened.pop()] = i
    return blocks

def parse(code):
    print("Parsing...")
    return ''.join(c for c in code if c in '><+-.,[]')


def run(code):
    code = parse(code)
    x = i = 0
    bf = {0: 0}
    blocks = block(code)
    l = len(code)
    while i < l:
        sym = code[i]
        if sym == '>':
            x = (x+1)%(300*100)
            bf.setdefault(x, 0)
        elif sym == '<':
            x = (x-1 + 300*100)%(300*100)
        elif sym == '+':
            bf[x] = (bf[x]+1)%256
        elif sym == '-':
            bf[x] = (256+bf[x]-1)%256
        elif sym == '.':
            print(chr(bf[x]), end='')
        elif sym == ',':
            print("# memory: ", end="")
            y = 0
            while bf[y]:
                print(chr(bf[y]), end="")
                y+=1
            #print()
            bitmap_work.bf_memory_to_image(bf)
            bf[x] = 66 #int(input('Input: '))
            for _ in bf.keys():
                bf[_] = 0
        elif sym == '[':
            try:
                if not bf[x]: i = blocks[i]
            except Exception as e:
                print(f"[: x={x} i={i}")
                raise(e)
        elif sym == ']':
            if bf[x]: i = blocks[i]
        i += 1

import sys
code = open(sys.argv[1]).read()
run(code)