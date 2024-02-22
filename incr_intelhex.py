#!/usr/bin/python3

import sys
import re

# print ('Num args:', len(sys.argv), 'arguments.')
# print ('Args:', str(sys.argv

numBytes = 2048
if len(sys.argv) > 1:
  argv = sys.argv[1]
  multiplier = 1
  if 'k' in argv.lower():
    multiplier = 1024
  elif 'm' in argv.lower():
    multiplier = 1024*1024
  
  argv = re.sub("[^0-9]", "", argv)  
  
  try:
      numBytes = int(argv)*multiplier
  except ValueError:
      numBytes = 0
 
# print(f"numBytes={numBytes}") 


def checksum(val):
  chksum = 0
  while len(val) > 0:
    byte = int(val[-2:], 16)
    chksum += byte
    val = val[:-2]
  chksum = (~chksum + 1) & 0xFF
  return f'{chksum:02x}'


def endian_swap32(x):
    return int.from_bytes(x.to_bytes(4, byteorder='little'), byteorder='big', signed=False)

# =============================================================

numwords = 4096

recsize = 8
addr = 0
rectype = 0

numWords = int(numBytes / 8)

# print(f"// Incrementing sequence 0f 32-bit values")
for i in range(0,numWords,2):
  aa = endian_swap32(i)
  bb = endian_swap32(i+1)
  rec = f"{recsize:02x}{addr:04x}{rectype:02x}{aa:08x}{bb:08x}"
  print(f":{rec}{checksum(rec)}")
  addr += recsize

# EOF
recsize = 0
addr = 0
rectype = 1
rec = f"{recsize:02x}{addr:04x}{rectype:02x}"
# rec=f"00000001"
print(f":{rec}{checksum(rec)}")

