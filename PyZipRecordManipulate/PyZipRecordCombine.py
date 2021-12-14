import struct
import os
import json

FilesDir = 'DATA_Records/ZIPFILERECORDS'
DirsDir = 'DATA_Records/ZIPDIRENTRIES'
END = 'DATA_Records/EOFRecord'

FileNameList = []
OldOffsets = []
FileOffsets = []

with open('DATA.lst', 'r') as f:
    for line in f.readlines():
        data = line.strip("\n").split(',')
        FileNameList.append(data[0])
        OldOffsets.append(int(data[1]))

baseKeyIndex = 0
with open('DATA_2.ZIP', 'wb') as f:
    print("Processing main files")
    for file in FileNameList:
        FileOffsets.append(f.tell())
        with open(FilesDir + '/' + file, 'rb') as i:
            f.write(i.read())
    print("Processing dir files")
    for file in FileNameList:
        with open(DirsDir + '/' + file, 'rb') as i:
            unimportant1 = i.read(42)
            f.write(unimportant1)
            f.write(struct.pack('I', FileOffsets[FileNameList.index(file)]))
            i.seek(4, 1)
            f.write(i.read())
    with open(END, 'rb') as i:
        f.write(i.read())
        
# This will take ages
with open('data.idx', 'r+b') as dataidx:
    dataidx.seek(0, 2)
    size = dataidx.tell()
    dataidx.seek(0x00)
    while dataidx.tell() < 0x082720:
        print((dataidx.tell() / 0x082720) * 100)
        tint = struct.unpack("I", dataidx.read(4))[0]
        if tint in OldOffsets:
            dataidx.seek(-4, 1)
            dataidx.write(struct.pack("I", FileOffsets[OldOffsets.index(tint)]))
    