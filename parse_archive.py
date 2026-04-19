#!/usr/bin/env python3
"""Step 2: Parse PyInstaller CArchive and list TOC entries"""
import struct, zlib

with open('pydata.bin', 'rb') as f:
    data = f.read()

MAGIC = b'MEI\014\013\012\013\016'
pos   = data.find(MAGIC)
print(f"[+] Magic found at offset: {pos}")

cookie  = data[pos:]
pkg_len = struct.unpack('>I', cookie[8:12])[0]
toc_off = struct.unpack('>I', cookie[12:16])[0]
toc_len = struct.unpack('>I', cookie[16:20])[0]
pyver   = struct.unpack('>I', cookie[20:24])[0]
print(f"[+] pkg_len={pkg_len}, toc_off={toc_off}, toc_len={toc_len}, pyver={pyver}")

archive_start = len(data) - pkg_len
toc_abs       = archive_start + toc_off
print(f"[+] archive_start={archive_start}, toc_abs={toc_abs}")
print()

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

print(f"[+] Found {len(entries)} TOC entries:")
for e in entries:
    print(f"    [{e[4]}] {e[5]:60s} csize={e[2]}")
