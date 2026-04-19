#!/usr/bin/env python3
"""Step 1: Extract pydata section from ELF binary"""
import struct, sys

filename = sys.argv[1] if len(sys.argv) > 1 else 'waiting_game'

with open(filename, 'rb') as f:
    data = f.read()

e_shoff     = struct.unpack('<Q', data[40:48])[0]
e_shentsize = struct.unpack('<H', data[58:60])[0]
e_shnum     = struct.unpack('<H', data[60:62])[0]
e_shstrndx  = struct.unpack('<H', data[62:64])[0]

shstr_sh  = e_shoff + e_shstrndx * e_shentsize
sh_offset = struct.unpack('<Q', data[shstr_sh+24:shstr_sh+32])[0]
sh_size   = struct.unpack('<Q', data[shstr_sh+32:shstr_sh+40])[0]
strtab    = data[sh_offset:sh_offset+sh_size]

for i in range(e_shnum):
    sh = e_shoff + i * e_shentsize
    name_idx = struct.unpack('<I', data[sh:sh+4])[0]
    name_end = strtab.find(b'\x00', name_idx)
    sname    = strtab[name_idx:name_end].decode('utf-8', errors='replace')

    if sname == 'pydata':
        off  = struct.unpack('<Q', data[sh+24:sh+32])[0]
        size = struct.unpack('<Q', data[sh+32:sh+40])[0]
        pydata = data[off:off+size]
        with open('pydata.bin', 'wb') as f2:
            f2.write(pydata)
        print(f"[+] Found pydata section: offset={off}, size={size}")
        print(f"[+] Saved to pydata.bin")
        break
else:
    print("[-] pydata section not found!")
