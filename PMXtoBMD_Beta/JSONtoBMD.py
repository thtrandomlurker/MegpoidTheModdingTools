import json
import struct
import sys

with open(sys.argv[1], 'r', encoding="UTF-8") as inf:
    with open(sys.argv[1].split('.')[0] + '.bmd', 'wb') as out:
        data = json.load(inf)
        out.write(b'B3D OBJECT DATA\x00\xCD\xCC\xCC\x3Dcomment')
        out.write(b'\x00' * 0x59)
        out.write(struct.pack("<I", data["B3DModel"]["PhysicsNumber"]))
        out.write(b'\x00' * 0x1C)
        out.write(struct.pack("<I", len(data["B3DModel"]["Textures"])))
        out.write(b'\x00' * 12)
        # I have no clue if these hashes are important so i'll just set them as a FourCC
        out.write(b'TEXT')
        for texName in data["B3DModel"]["Textures"]:
            print(texName)
            out.write(texName.encode("Shift-JIS") + b'\x00' * (32 - len(texName.encode("Shift-JIS"))))
        out.write(struct.pack("<I", len(data["B3DModel"]["Materials"])))
        out.write(b'\x00' * 12)
        # I have no clue if these hashes are important so i'll just set them as a FourCC
        out.write(b'MATE')
        for material in data["B3DModel"]["Materials"]:
            out.write(struct.pack("<I", material["s1"]))
            out.write(struct.pack("<H", material["s2"]))
            out.write(struct.pack("<H", data["B3DModel"]["Textures"].index(material["TexName"])))
            out.write(struct.pack("BBBB", material["Diffuse"][0], material["Diffuse"][1], material["Diffuse"][1], material["Diffuse"][3]))
            out.write(struct.pack("BBBB", material["Ambient"][0], material["Ambient"][1], material["Ambient"][1], material["Ambient"][3]))
            out.write(struct.pack("BBBB", material["Specular"][0], material["Specular"][1], material["Specular"][1], material["Specular"][3]))
        out.write(struct.pack("<I", len(data["B3DModel"]["Bones"])))
        out.write(b'\x00' * 12)
        # I have no clue if these hashes are important so i'll just set them as a FourCC
        out.write(b'BONE')
        for bone in data["B3DModel"]["Bones"]:
            out.write(bone["Name"].encode("Shift-JIS") + b'\x00' * (32 - len(bone["Name"].encode("Shift-JIS"))))
            for Vector in bone["BoneMatrix"]:
                out.write(struct.pack("<ffff", Vector[0], Vector[1], Vector[2], Vector[3]))
            out.write(struct.pack("<ffff", bone["BonePosition"][0], bone["BonePosition"][1], bone["BonePosition"][2], bone["BonePosition"][3]))
            out.write(struct.pack("<I", bone["unk0"]))
            out.write(struct.pack("<h", bone["ParentID"]))
            out.write(struct.pack("<h", bone["ChildID"]))
            out.write(struct.pack("<I", bone["unk1"]))
            out.write(struct.pack("<I", bone["unk2"]))
        # Only test.bmd uses this so
        out.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00IKND')
        out.write(struct.pack("<I", len(data["B3DModel"]["VertexSets"])))
        for vertexSet in data["B3DModel"]["VertexSets"]:
            out.write(b"VSET")
            out.write(struct.pack("<H", vertexSet["unk1"]))
            out.write(struct.pack("<H", len(vertexSet["Vertices"])))
            out.write(struct.pack("<I", vertexSet["unk2"]))
            out.write(struct.pack("<I", vertexSet["unk3"]))
            out.write(struct.pack("<I", vertexSet["unk4"]))
        # repeat
        curVertIndex = 0
        out.write(b'VERT')
        for vertexSet in data["B3DModel"]["VertexSets"]:
            for vertex in vertexSet["Vertices"]:
                out.write(struct.pack("<fff", vertex["Pos"][0], vertex["Pos"][1], vertex["Pos"][2]))
                out.write(struct.pack("<fff", vertex["NormalDir"][0], vertex["NormalDir"][1], vertex["NormalDir"][2]))
                out.write(struct.pack("<ff", vertex["UVCoord"][0], vertex["UVCoord"][1]))
                out.write(struct.pack("BBBB", vertex["VertexColor"][0], vertex["VertexColor"][1], vertex["VertexColor"][2], vertex["VertexColor"][3]))
                out.write(struct.pack("BBBB", vertex["Bone0"], vertex["Bone1"], vertex["Bone2"], vertex["Bone3"]))
                out.write(struct.pack("<ffff", vertex["Weight0"], vertex["Weight1"], vertex["Weight2"], vertex["Weight3"]))
                out.write(struct.pack("<I", vertex["VertID"]))
        out.write(struct.pack("<I", len(data["B3DModel"]["FaceSets"])))
        for faceSet in data["B3DModel"]["FaceSets"]:
            out.write(b"FSET")
            out.write(struct.pack("<I", faceSet["Idx"]))
            out.write(struct.pack("<H", len(faceSet["FaceIndices"])))
            out.write(struct.pack("<H", faceSet["unk1"]))
            out.write(struct.pack("<H", len(faceSet["FaceBones"])))
            out.write(struct.pack("<H", faceSet["unk2"]))
            out.write(struct.pack("<H", faceSet["MatID"]))
            out.write(struct.pack("<H", faceSet["unk3"]))
            out.write(struct.pack("<I", faceSet["unk4"]))
        out.write(b'FACE')
        for faceSet in data["B3DModel"]["FaceSets"]:
            for index in faceSet["FaceIndices"]:
                out.write(struct.pack("<H", index))
            for bone in faceSet["FaceBones"]:
                out.write(struct.pack("<H", bone))
        out.write(struct.pack("<I", len(data["B3DModel"]["MorphData"])))
        out.write(b'\x00' * 12)
        for morph in data["B3DModel"]["MorphData"]:
            out.write(b"MRPH")
            out.write(morph["Name"].encode("Shift-JIS") + b'\x00' * (32 - len(morph["Name"].encode("Shift-JIS"))))
            out.write(struct.pack("<I", morph["Panel"]))
            out.write(struct.pack("<I", len(morph["VertTranslations"])))
        out.write(b"VTRA")
        for morph in data["B3DModel"]["MorphData"]:
            for vertTranslation in morph["VertTranslations"]:
                out.write(struct.pack("<Ifff", vertTranslation[0], vertTranslation[1], vertTranslation[2], vertTranslation[3]))