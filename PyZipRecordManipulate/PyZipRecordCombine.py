import struct
import os

FilesDir = 'DATA_Records/ZIPFILERECORDS'
DirsDir = 'DATA_Records/ZIPDIRENTRIES'
END = 'DATA_Records/EOFRecord'

FileNameList = []
FileOffsets = []

with open('DATA.lst', 'r') as f:
    for line in f.readlines():
        FileNameList.append(line.strip('\n'))

with open('DATA_2.ZIP', 'wb') as f:
    for file in FileNameList:
        FileOffsets.append(f.tell())
        with open(FilesDir + '/' + file, 'rb') as i:
            f.write(i.read())
    for file in FileNameList:
        with open(DirsDir + '/' + file, 'rb') as i:
            unimportant1 = i.read(42)
            f.write(unimportant1)
            f.write(struct.pack('I', FileOffsets[FileNameList.index(file)]))
            i.seek(4, 1)
            f.write(i.read())
    with open(END, 'rb') as i:
        f.write(i.read())