import struct
import json
import copy
import sys

def ReadPMXString(file):
    stringSize = struct.unpack("I", file.read(4))[0]
    string = file.read(stringSize).decode("UTF-16-LE")
    return string

with open(sys.argv[1], 'rb') as inf:
    with open(sys.argv[1].split('.')[0] + '.json', 'w', encoding="UTF-8") as out:
        outDict = {"B3DModel": {"PhysicsNumber": 1, "Textures": [], "Materials": [], "Bones": [], "VertexSets": [], "FaceSets": [], "MorphData": []}}
        Signature = inf.read(4)
        Version = struct.unpack("f", inf.read(4))[0]
        GlobalsCount = inf.read(1)[0]
        Encoding = inf.read(1)[0]
        AddVec4Count = inf.read(1)[0]
        VertIndexSize = inf.read(1)[0]
        if VertIndexSize == 1:
            vis = "b"
        elif VertIndexSize == 2:
            vis = "h"
        elif VertIndexSize == 4:
            vis = "i"
        TextureIndexSize = inf.read(1)[0]
        if TextureIndexSize == 1:
            tis = "b"
        elif TextureIndexSize == 2:
            tis = "h"
        elif TextureIndexSize == 4:
            tis = "i"
        MaterialIndexSize = inf.read(1)[0]
        if MaterialIndexSize == 1:
            mtis = "b"
        elif MaterialIndexSize == 2:
            mtis = "h"
        elif MaterialIndexSize == 4:
            mtis = "i"
        BoneIndexSize = inf.read(1)[0]
        if BoneIndexSize == 1:
            bis = "b"
        elif BoneIndexSize == 2:
            bis = "h"
        elif BoneIndexSize == 4:
            bis = "i"
        MorphIndexSize = inf.read(1)[0]
        if MorphIndexSize == 1:
            mpis = "b"
        elif MorphIndexSize == 2:
            mpis = "h"
        elif MorphIndexSize == 4:
            mpis = "i"
        RigidBodyIndexSize = inf.read(1)[0]
        if RigidBodyIndexSize == 1:
            rbs = "b"
        elif RigidBodyIndexSize == 2:
            rbs = "h"
        elif RigidBodyIndexSize == 4:
            rbs = "i"
        n1 = ReadPMXString(inf)
        n2 = ReadPMXString(inf)
        d1 = ReadPMXString(inf)
        d2 = ReadPMXString(inf)
        Vertices = []
        VertCount = struct.unpack("i", inf.read(4))[0]
        for i in range(VertCount):
            vertPos = list(struct.unpack("fff", inf.read(12)))
            vertNormal = list(struct.unpack("fff", inf.read(12)))
            vertUV = list(struct.unpack("ff", inf.read(8)))
            vertIndices = [0] * 4
            vertWeights = [0.0] * 4
            inf.seek(16 * AddVec4Count, 1)
            deformType = inf.read(1)
            if deformType == b'\x00':
                BoneIndex = struct.unpack(bis, inf.read(BoneIndexSize))[0]
                Weight = 1.0
                vertIndices[0] = BoneIndex
                vertWeights[0] = Weight
            elif deformType == b'\x01':
                BoneIndex1 = struct.unpack(bis, inf.read(BoneIndexSize))[0]
                BoneIndex2 = struct.unpack(bis, inf.read(BoneIndexSize))[0]
                Weight1 = struct.unpack("f", inf.read(4))[0]
                Weight2 = 1.0 - Weight1
                vertIndices[0] = BoneIndex1
                vertIndices[1] = BoneIndex2
                vertWeights[0] = Weight1
                vertWeights[1] = Weight2
            elif deformType == b'\x02':
                BoneIndex1 = struct.unpack(bis, inf.read(BoneIndexSize))[0]
                BoneIndex2 = struct.unpack(bis, inf.read(BoneIndexSize))[0]
                BoneIndex3 = struct.unpack(bis, inf.read(BoneIndexSize))[0]
                BoneIndex4 = struct.unpack(bis, inf.read(BoneIndexSize))[0]
                Weight1 = struct.unpack("f", inf.read(4))[0]
                Weight2 = struct.unpack("f", inf.read(4))[0]
                Weight3 = struct.unpack("f", inf.read(4))[0]
                Weight4 = struct.unpack("f", inf.read(4))[0]
                vertIndices[0] = BoneIndex1
                vertIndices[1] = BoneIndex2
                vertIndices[2] = BoneIndex3
                vertIndices[3] = BoneIndex4
                vertWeights[0] = Weight1
                vertWeights[1] = Weight2
                vertWeights[2] = Weight3
                vertWeights[3] = Weight4
            else:
                print("Unsupported skinning method. Exiting")
                exit()
            EdgeScale = struct.unpack("f", inf.read(4))[0]
            # Get stuff into a supported vertex format ahead of time
            Vertices.append({"Pos": vertPos, "NormalDir": vertNormal, "UVCoord": vertUV, "VertexColor": [255, 255, 255, 255], "Bone0": vertIndices[0], "Bone1": vertIndices[1], "Bone2": vertIndices[2], "Bone3": vertIndices[3], "Weight0": vertWeights[0], "Weight1": vertWeights[1], "Weight2": vertWeights[2], "Weight3": vertWeights[3], "VertID": i})
        CombinedIndexList = []
        TotalFaceCount = struct.unpack("i", inf.read(4))[0]
        for i in range(TotalFaceCount):
            CombinedIndexList.append(struct.unpack(vis, inf.read(VertIndexSize))[0])
        TextureList = []
        TexturePathCount = struct.unpack("i", inf.read(4))[0]
        for i in range(TexturePathCount):   
            TextureList.append(ReadPMXString(inf))
        # print(TextureList)  # Ensure we're getting here, which we are
        # Bookmark, the above is known working
        Materials = []
        FaceSets = []
        MaterialCount = struct.unpack("i", inf.read(4))[0]
        BaseMaterialFaceOffset = 0
        for i in range(MaterialCount):
            MaterialName = ReadPMXString(inf)
            MaterialNameUniversal = ReadPMXString(inf)
            Diffuse = list(struct.unpack("ffff", inf.read(16)))
            Specular = list(struct.unpack("ffff", inf.read(16)))
            Ambient = list(struct.unpack("fff", inf.read(12)))
            print(Ambient)
            DrawFlags = inf.read(1)
            EdgeColor = list(struct.unpack("ffff", inf.read(16)))
            EdgeScale = struct.unpack("f", inf.read(4))[0]
            TextureIndex = struct.unpack(tis, inf.read(TextureIndexSize))[0]
            SphereIndex = struct.unpack(tis, inf.read(TextureIndexSize))[0]
            SphereMode = inf.read(1)[0]
            ToonReference = inf.read(1)[0]
            if ToonReference == 0:
                ToonIndex = struct.unpack(tis, inf.read(TextureIndexSize))[0]
            elif ToonReference == 1:
                ToonIndex = inf.read(1)[0]
            else:
                print("Malformed PMX File. Exiting.")
                exit()
            Metadata = ReadPMXString(inf)
            SurfaceCount = struct.unpack("i", inf.read(4))[0]
            FaceSet = {"unk0": 0, "Idx": i, "FaceCount": SurfaceCount, "unk1": 0, "FaceBoneCount": None, "unk2": 0, "MatID": i, "unk3": 0, "unk4": 0, "FaceIndices": CombinedIndexList[BaseMaterialFaceOffset:BaseMaterialFaceOffset+SurfaceCount], "FaceBones": []}
            Material = {"s1": 4606, "s2": 255, "TexName": TextureList[TextureIndex], "Diffuse": [int(Diffuse[0] * 255), int(Diffuse[1] * 255), int(Diffuse[2] * 255), int(Diffuse[3] * 255)], "Ambient": [int(Ambient[0] * 255), int(Ambient[1] * 255), int(Ambient[2] * 255), 255], "Specular": [int(Specular[0] * 255), int(Specular[1] * 255), int(Specular[2] * 255), 255]}
            Materials.append(Material)
            FaceSets.append(FaceSet)
            BaseMaterialFaceOffset += SurfaceCount
        Bones = []
        BoneCount = struct.unpack("i", inf.read(4))[0]
        print(BoneCount)
        for i in range(BoneCount):
            BoneName = ReadPMXString(inf)
            print(BoneName)
            BoneNameUniversal = ReadPMXString(inf)
            Position = list(struct.unpack("fff", inf.read(12)))
            Parent = struct.unpack(bis, inf.read(BoneIndexSize))[0]
            DeformLayer = struct.unpack("i", inf.read(4))[0]
            fb1 = inf.read(1)[0]
            fb2 = inf.read(1)[0]
            flags = list(format(fb2, 'b').zfill(8) + format(fb1, 'b').zfill(8))
            flags.reverse()
            if flags[0] == '1':
                inf.seek(BoneIndexSize, 1)
            else:
                inf.seek(12, 1)
            if flags[8] == '1' or flags[9] == '1':
                inf.seek(BoneIndexSize, 1)
                inf.seek(4, 1)
            if flags[10] == '1':
                inf.seek(12, 1)
            if flags[11] == '1':
                inf.seek(8, 1)
            if flags[13] == '1':
                inf.seek(BoneIndexSize, 1)
            if flags[5] == '1':
                print("IK used. too lazy to handle. exiting")
                exit()
            Bone = {"Name": BoneName, "BoneMatrix": [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], list(Position) + [1.0]], "BonePosition": list(Position) + [0.0], "unk0": 0, "ParentID": Parent, "ChildID": 0, "unk1": 0, "unk2": 0}
            Bones.append(Bone)
        Morphs = []
        ## build base morph
        #baseMorph = {"Name": "base", "Panel": 0, "VertCount": len(Vertices), "VertTranslations": []}
        #for index, vert in enumerate(Vertices):
        #    baseMorph["VertTranslations"].append([index, vert["Pos"][0], vert["Pos"][1], vert["Pos"][2]])
        #Morphs.append(baseMorph)
        #preMorphTell = inf.tell()
        #MorphCount = struct.unpack("I", inf.read(4))[0]
        #for i in range(MorphCount):
        #    Morph = {"Name": "", "Panel": 0, "VertCount": 0, "VertTranslations": []}
        #    Morph["Name"] = ReadPMXString(inf)
        #    MorphNameEN = ReadPMXString(inf)
        #    Morph["Panel"] = inf.read(1)[0]
        #    MorphType = inf.read(1)[0]
        #    Morph["VertCount"] = struct.unpack("I", inf.read(4))[0]
        #    for o in range(Morph["VertCount"]):
        #        vIndex = struct.unpack(vis, inf.read(VertIndexSize))[0]
        #        translation = struct.unpack("fff", inf.read(12))
        #        Morph["VertTranslations"].append([vIndex, translation[0], translation[1], translation[2]])
        #    Morphs.append(Morph)
            
        VertexSets = []
        BaseSubtract = 0
        for i in range(MaterialCount):
            FaceSet = FaceSets[i]
            VtxSetVerts = []
            newIndices = []
            processedIndices = []
            usedBoneIndices = []
            idx = 0
            for index in FaceSet["FaceIndices"]:
                VertCopy = copy.deepcopy(Vertices[index])
                if VertCopy in VtxSetVerts:
                    newIndices.append(VtxSetVerts.index(VertCopy))
                else:
                    VtxSetVerts.append(VertCopy)
                    newIndices.append(idx)
                    idx += 1
            for idx, vert in enumerate(VtxSetVerts):
                if vert["Bone0"] not in usedBoneIndices:
                    usedBoneIndices.append(vert["Bone0"])
                if vert["Bone1"] not in usedBoneIndices:
                    usedBoneIndices.append(vert["Bone1"])
                if vert["Bone2"] not in usedBoneIndices:
                    usedBoneIndices.append(vert["Bone2"])
                if vert["Bone3"] not in usedBoneIndices:
                    usedBoneIndices.append(vert["Bone3"])
                src0 = vert["Bone0"]
                src1 = vert["Bone1"]
                src2 = vert["Bone2"]
                src3 = vert["Bone3"]
                VtxSetVerts[idx]["Bone0"] = usedBoneIndices.index(src0)
                VtxSetVerts[idx]["Bone1"] = usedBoneIndices.index(src1)
                VtxSetVerts[idx]["Bone2"] = usedBoneIndices.index(src2)
                VtxSetVerts[idx]["Bone3"] = usedBoneIndices.index(src3)
            print(usedBoneIndices)
            # this might get complicated. i need to check the number of bones used, and split if it's too high.
            if len(usedBoneIndices) > 8:  # i know for a fact 8 works as intended
                AppxOverFlow = (len(usedBoneIndices) // 8) + 1
                print(AppxOverFlow)
            VertexSet = {"unk0": 0, "unk1": 0, "VtxCount": len(VtxSetVerts), "unk2": 0, "unk3": 0, "unk4": 0, "Vertices": VtxSetVerts}
            FaceSet["FaceIndices"] = newIndices
            FaceSet["FaceBones"] = usedBoneIndices
            FaceSet["FaceBoneCount"] = len(usedBoneIndices) # allow all bones
            outDict["B3DModel"]["FaceSets"].append(FaceSet)
            outDict["B3DModel"]["VertexSets"].append(VertexSet)
        outDict["B3DModel"]["Bones"] = Bones
        outDict["B3DModel"]["Textures"] = TextureList
        outDict["B3DModel"]["Materials"] = Materials
        outDict["B3DModel"]["MorphData"] = Morphs
        
        json.dump(outDict, out, indent=2, ensure_ascii=False)
            
                
            
            
            
            
            
            
            
            