import sys
import random
import bitmap_work

def screen_print(param):
    """Выводит сообщение в stdout"""
    ans = []
    param+="\n"
    ans.append("[-]")
    last_byte = "\x00"
    for i in param:
        ans.append(
            "+"*(ord(i)-ord(last_byte))
                   )
        ans.append(
            "-"*(ord(last_byte)-ord(i))
                   )
        last_byte = i
        ans.append(".")
    return ans

def mem_print_with_single_pause(param):
    "Выводит сообщение, останавливаясь в конце"
    ans = []
    param+="\n\x00"
    ans.append("<")
    for i in param:
        ans.append(">[-]")
        ans.append(
            "+"*(ord(i))
        )
    ans.append("<"*(len(param)-1) + ",")
    return ans

def draw_image(param):
    ans = []
    bm = bitmap_work.image_to_bitmap(imagepath=param)
    assert len(bm) == 300*100
    for i in range(len(bm)):
        ans.append("+"*bm[i]+">")
    return ans

def optimice(ans):
    print("Optimice started")
    anz = "".join(ans)
    before = len(anz)
    while "><" in anz:
        anz = anz.replace("><", "")
    while "<>" in anz:
        anz = anz.replace("<>", "")
    #for i in reversed(range(15000, 30000)):
    #    anz = anz.replace("<" * i, ">"*(30000-i))
    #    anz = anz.replace(">" * i, "<"*(30000-i))
    print("Optimice ended")
    after = len(anz)
    print("Compression ratio after/before:", after/before)

    return [anz]

def draw_with_pauses(param):
    ans = []
    for symbol in param:
        bm = bitmap_work.image_to_bitmap(text=symbol)
        assert len(bm) == 300*100
        for i in range(len(bm)):
            #print(i)
            ans.append("+"*bm[i])
            ans.extend(trash(1))
            ans.append(">")
        ans.append(",")
    #ans = optimice(ans)
    return ans


def _move(b):

    to_b = ">"*b if b>0 else "<"*abs(b)
    from_b = "<"*b if b>0 else ">"*abs(b)
    ret = to_b + "[-]" + from_b + "[-" + to_b + "+" + from_b + "]"
    #print("res of move", b, ret)
    return ret

def trash(count_of_trash):
    "Создает обфускационные вставки"
    count_of_trash = int(count_of_trash)
    ans = []
    for i in range(count_of_trash):
        r = random.randint(0, 13)
        #r = 3
        if r in [0,1,2]:
            ans.append("+"*256)
        elif r == [3,4,5]:
            ans.append("-"*256)
        elif r == [6,7,8]:
            _ = random.randrange(10, 20)
            ans.append("+"*_ + "-"*_)
        elif r == [9]:
            _ = random.randrange(10, 20)
            ans.append(_move(_))
            ans.append(">"*_)
            ans.append(_move(-_))
            ans.append("<"*_)
        elif r == [10,11,12]:
            for j in range(8):
                _ = random.randrange(2, 20)
                ans.append(">"*_)
                ans.append("<"*_)
    return ans


registered_operations = {
    "mem_print_with_single_pause": mem_print_with_single_pause,
    "screen_print": screen_print,
    "trash": trash,
    "draw_with_pauses": draw_with_pauses,
    "draw_image": draw_image
}

def compile(text):
    output = []

    for line in text.split("\n"):
        if not len(line) or line[0] == "#":
            continue
        instr = line.split(" ", maxsplit=1)
        param = ""
        if len(instr) > 1:
            param = instr[1]
        instr = instr[0]
        print(instr, "'", param)

        if instr in registered_operations.keys():
            output.extend(registered_operations[instr](param))
        else:
            print("NOT IMPLEMENTED, OMIT")
    #print("Reducing ''")
    #while "" in output:
    #    output.remove("")
    print("Saving...")
    open(sys.argv[1] + ".bf2", "w").write("\n".join(output))

if __name__ == "__main__":
    compile(open(sys.argv[1]).read())