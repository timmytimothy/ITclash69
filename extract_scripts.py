#!/usr/bin/env python3
"""Step 3: Extract and decompress all Python scripts from archive"""
import struct, zlib, os

with open('pydata.bin', 'rb') as f:
    data = f.read()

MAGIC = b'MEI\014\013\012\013\016'
pos   = data.find(MAGIC)

cookie  = data[pos:]
pkg_len = struct.unpack('>I', cookie[8:12])[0]
toc_off = struct.unpack('>I', cookie[12:16])[0]
toc_len = struct.unpack('>I', cookie[16:20])[0]

archive_start = len(data) - pkg_len
toc_abs       = archive_start + toc_off

i = toc_abs
entries = []
while i < toc_abs + toc_len:
    entry_size = struct.unpack('>I', data[i:i+4])[0]
    if entry_size == 0 or i + entry_size > len(data):
        break
    d_offset = struct.unpack('>I', data[i+4:i+8])[0]
    csize    = struct.unpack('>I', data[i+8:i+12])[0]
    usize    = struct.unpack('>I', data[i+12:i+16])[0]
    cflag    = data[i+16]
    typecode = chr(data[i+17])
    name     = data[i+18:i+entry_size].rstrip(b'\x00').decode('utf-8', errors='replace')
    entries.append((d_offset, csize, usize, cflag, typecode, name))
    i += entry_size

os.makedirs('extracted', exist_ok=True)

for (d_offset, csize, usize, cflag, typecode, name) in entries:
    if typecode in ('s', 'm', 'M'):
        raw = data[archive_start + d_offset:archive_start + d_offset + csize]
        if cflag:
            raw = zlib.decompress(raw)
        ext   = '.pyc' if typecode in ('m', 'M') else '.py'
        fname = f"extracted/{name.replace('/', '_')}{ext}"
        with open(fname, 'wb') as f2:
            f2.write(raw)
        print(f"[+] Extracted [{typecode}] {name} -> {fname} ({len(raw)} bytes)")

print("\n[+] Done! Check ./extracted/")
print("\n[*] To find flag:")
print('   type extracted\\waiting_game.py | findstr "Cl@sh"')

