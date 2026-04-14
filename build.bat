@echo off
REM // should match
copy "rom.gen" "rom.bin"
python.exe romcmp.py "rom.gen" "rom.bin"
REM // if checksum wasn't already calculated, shouldn't match
python.exe rompatch.py "rom.gen" "rom.bin" 0x0
python.exe romcmp.py "rom.gen" "rom.bin"

pause & exit