import pyshark
import idna

cap = pyshark.FileCapture("forensic.pcapng", display_filter="dns")
cap.load_packets()

flag = ""

for i in cap:
    if "xn--" in i.dns.qry_name:
        tmp = idna.decode(i.dns.qry_name)
        for j in range(len(tmp)):
            if(ord(tmp[j])<0x7f and tmp[j]!="."):
                flag+=tmp[j]

print(b"".fromhex(flag[::4]))
