"""
Compare two files and ensure they're identical
usage: rompatcher.py romold romnew
"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("romold")
parser.add_argument("romnew")
args = parser.parse_args()

bufold = bytearray()
bufnew = bytearray()
with open(args.romold,"r+b") as rom: bufold.extend(rom.read())
with open(args.romnew,"r+b") as rom: bufnew.extend(rom.read())
if len(bufold) != len(bufnew):
    print("size of old rom and new rom do not match")
    print("old:",len(bufold))
    print("new:",len(bufnew))

iterate = 0
if len(bufold) < len(bufnew):
    smallestbuffer = len(bufold)
else:
    smallestbuffer = len(bufnew)
while iterate < smallestbuffer:
    if bufold[iterate] != bufnew[iterate]:
        print("byte",hex(iterate),"does not match! old =",hex(bufold[iterate]),"new =",hex(bufnew[iterate]))
    iterate += 1
exit()
