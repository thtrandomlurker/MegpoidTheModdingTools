import struct
import os
if not os.path.exists('DATA_Records/ZIPFILERECORDS'):
    os.makedirs('DATA_Records/ZIPFILERECORDS')
if not os.path.exists('DATA_Records/ZIPDIRENTRIES'):
    os.makedirs('DATA_Records/ZIPDIRENTRIES')
    
ParsedFileEntries = 0
ParsedDirEntries = 0
FileNameList = []
FilePathList = []
FileOffsetList = []

with open('DATA.ZIP', 'rb') as f:
    while True:
        FileOffsetList.append(f.tell())
        ZipRecordType = f.read(4)
        if ZipRecordType == b'PK\x03\x04': # Standard ZIPFILERECORD
            RecordData = b'PK\x03\x04'
            RecordData += f.read(18)
            fsBytes = f.read(4)
            fileSize = struct.unpack('I', fsBytes)[0]
            RecordData += fsBytes
            FileNameLengthBytes = f.read(2)
            FileNameLength = struct.unpack('H', FileNameLengthBytes)[0]
            RecordData += FileNameLengthBytes
            RecordData += f.read(2)
            FileNameBytes = f.read(FileNameLength)
            FileName = FileNameBytes.decode('ASCII')
            FilePathList.append(FileName)
            RecordData += FileNameBytes
            RecordData += f.read(fileSize)
            with open(f'DATA_Records/ZIPFILERECORDS/{FileName.replace("/", "")}', 'wb') as o:
                o.write(RecordData)
            FileNameList.append(FileName.replace("/", ""))
            ParsedFileEntries += 1
        elif ZipRecordType == b'PK\x01\x02':
            RecordData = b'PK\x01\x02'
            RecordData += f.read(20)
            FsBytes = f.read(4)
            Fs = struct.unpack('I', FsBytes)[0]
            RecordData += FsBytes
            FNLenBytes = f.read(2)
            FNLen = struct.unpack('H', FNLenBytes)[0]
            RecordData += FNLenBytes
            RecordData += f.read(16)
            FN = f.read(FNLen)
            RecordData += FN
            with open(f'DATA_Records/ZIPDIRENTRIES/{FN.decode("ASCII").replace("/", "")}', 'wb') as o:
                o.write(RecordData)
            ParsedDirEntries += 1
        elif ZipRecordType == b'PK\x05\x06':
            RecordData = b'PK\x05\x06'
            RecordData += f.read(18)
            with open('DATA_Records/EOFRecord', 'wb') as o:
                o.write(RecordData)
            break
            
    with open('DATA.lst', 'w') as o:
        for idx, file in enumerate(FileNameList):
            o.write(f"{file}, {FileOffsetList[idx]}\n")
            
            