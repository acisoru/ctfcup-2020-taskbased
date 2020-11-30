import base64
a = open("real_executable.py", "rb").read()
b = "import base64;exec(base64.b64decode('"+base64.b64encode(a).decode()+"'))"
open("real_executable.b64.py", "w").write(b)