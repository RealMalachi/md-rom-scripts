"""
patch a mega drive rom after it's been built
usage: rompatcher.py romin romout padto
romin is the input rom
romout is the output rom
padto is the hexadecimal (0x syntax) value you wish to pad the rom up to, 0 if you don't want any padding
TODO: option to hard-code the headers romend, namely to 0x3FFFFF
      rom end is how much rom the cartridge maps to the system, not the overall size of the rom
      This distinction matters for mappers like SSF2
TODO: option to disable time, in case they want to use that rom space for something else
"""
import argparse
import time
parser = argparse.ArgumentParser()
parser.add_argument("romin")
parser.add_argument("romout")
parser.add_argument("padto")
args = parser.parse_args()
checksum_std = 0

# start rom patching
with open(args.romin,"r+b") as openrom:
    buffer = bytearray()
    buffer.extend(openrom.read())

# pad rom
padtoaddr = int(args.padto,16)
print("padfrom:",hex(len(buffer)))
print("padto:",hex(padtoaddr))
while len(buffer) < padtoaddr:
    buffer.append(0x69)

# initialize romend and checksums
if len(buffer) < 0x200:
	print("ERROR: Rom size (",hex(len(buffer)),") is smaller then the header, exitting the rom patcher to avoid out-of-bound writes")
	exit()
romend = len(buffer)-1
romendmap = romend
print("romend:",hex(romend))
buffer[0x1A4] = 0x00
buffer[0x1A5] = romendmap >>16 & 0xFF
buffer[0x1A6] = romendmap >>8 & 0xFF
buffer[0x1A7] = romendmap & 0xFF
buffer[0x18E] = 0x00
buffer[0x18F] = 0x00

# set build time
# DD/MMM/YYYYzZZZZ
# HH-MM-SS________ (underscores to represent spaces)
date = time.strftime("%d/%b/%Y%z%X        ",time.gmtime())
print("date/time:",date)
iterate = 0
while iterate < len(date):
    buffer[iterate+0x40] = ord(date[iterate])
    iterate += 1

# calc standard
if len(buffer) % 2 != 0:
	print("ERROR: Rom size (",hex(len(buffer)),") isn't aligned by 2 bytes which is necessary for the standard checksum")
	exit()
iterate = 0x200
while iterate < romend:
    checksum_std += buffer[iterate]<<8 | buffer[iterate+1]
#    checksum_std &= 0xFFFF
    iterate += 2
print("std:",hex(checksum_std))
buffer[0x18E] = checksum_std >>8 & 0xFF
buffer[0x18F] = checksum_std & 0xFF 

# finish up
with open(args.romout,"w+b") as openrom:
    openrom.write(buffer)
exit()
