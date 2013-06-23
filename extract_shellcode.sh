#!/bin/sh
#Author: peternguyen
#extract shellcode from binary file
filename=$1
for i in `xxd -i $filename.bin | grep -v '\;' | grep -v unsigned | sed s/" "/" "/ | sed s/","/""/g | sed s/"0x"/"\\\\x"/g`
do
    echo "Write to "$filename.shellcode
    echo -n "\\$i" >> $filename.shellcode
    echo -n "\\$i"
done