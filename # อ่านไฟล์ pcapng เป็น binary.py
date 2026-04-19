# อ่านไฟล์ pcapng เป็น binary
with open('C:\COODEEE\CTFTESTPLACE\challenge.pcapng', 'rb') as f:
    data = f.read()

# ค้นหา printable strings ด้วย regex
import re
strings = re.findall(rb'[ -~]{6,}', data)
for s in strings:
    print(s.decode('ascii', errors='replace'))