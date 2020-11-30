import sys, time

if len(sys.argv) == 3 and sys.argv[1] == "please_stop_this_madness":
    flag = sys.argv[2]
    if flag.startswith("ctfcup{") and flag.endswith("}"):
        print("Da?")
        flag = [ord(i) for i in flag]
        if flag[24] - flag[20] == 20 and flag[17] - flag[16] == 47 and flag[30] - flag[7] == -6 and flag[27] - flag[7] == -49 and flag[22] - flag[18] == 70 and flag[21] - flag[15] == 31 and flag[26] - flag[9] == 7 and flag[25] - flag[31] == -28 and flag[28] - flag[20] == -14 and flag[11] - flag[29] == -34 and flag[23] - flag[14] == -3 and flag[15] - flag[18] == 0 and flag[19] - flag[18] == 33 and flag[7] - flag[16] == 37 and flag[20] - flag[29] == 9 and flag[9] - flag[8] == 51 and flag[10] - flag[8] == 19 and flag[31] - flag[8] == 50 and flag[13] - flag[18] == 44 and flag[8] - flag[18] == -2 and flag[14] - flag[16] == 16 and flag[18] - flag[16] == -16 and flag[29] - flag[12] == -24 and flag[12] - flag[16] == 43:
            print("DA!")
            exit(1337)