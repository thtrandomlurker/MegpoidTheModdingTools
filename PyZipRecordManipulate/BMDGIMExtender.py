import os

if input(f"This will eat a lot of drive space: ") == "Yes":
    for file in os.listdir("DATA_Records/ZIPFILERECORDS"):
        print(file)
        if "OBJECTSOBJ_MIGU" in file:
            with open(f"DATA_Records/ZIPFILERECORDS/{file}", 'r+b') as f:
                f.seek(0, 2)
                size = f.tell()
                if ".GIM" in file:
                    f.write(b'\x00' * (1048576 - size))
                elif ".BMD" in file:
                    f.write(b'\x00' * (2097152 - size))