import struct
import json

dummy_interpolation = b'\x14\x14\x00\x00\x14\x14\x14\x14\x6B\x6B\x6B\x6B\x6B\x6B\x6B\x6B\x14\x14\x14\x14\x14\x14\x14\x6B\x6B\x6B\x6B\x6B\x6B\x6B\x6B\x00\x14\x14\x14\x14\x14\x14\x6B\x6B\x6B\x6B\x6B\x6B\x6B\x6B\x00\x00\x14\x14\x14\x14\x14\x6B\x6B\x6B\x6B\x6B\x6B\x6B\x6B\x00\x00\x00'
dummy_rotation = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
dummy_position = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

class ANMHead(object):
    def ANMHead(self):
        self.magic
        self.unk01
        self.unk02
        self.unk03
        self.unk04
        self.unk05
        self.unk06

class MTNHead(object):
    def MTNHead(self):
        self.magic
        self.unk01
        self.unk02
        self.unk03
        self.unk04
        self.BoneCount
        self.unk05

class SKNHead(object):
    def SKNHead(self):
        self.magic
        self.unk01
        self.unk02
        self.unk03
        sekf.MorphCount
        self.unk04
        self.unk05

class MTNBoneDef(object):
    def MTNBoneDef(self):
        self.Name
        self.FrameCount
        self.Index
        self.unk01
        self.Type
        self.Hash01
        self.hash02
        
class MorphDef(object):
    def MorphDef(self):
        self.Name
        self.Index
        self.FrameCount
        self.unk01
        self.unk02
        
class PositionFrame(object):
    def PositionFrame(self):
        self.X
        self.Y
        self.Z
        self.Unk
        
class RotationFrame(object):
    def RotationFrame(self):
        self.X
        self.Y
        self.Z
        self.W
        
class Material(object):
    def Material(self):
        self.s1
        self.s2
        self.TexName
        self.Diffuse
        self.Ambient
        self.Specular
        
class Bone(object):
    def Bone(self):
        self.Name
        self.BoneMatrix
        self.BonePosition
        self.unk0
        self.ParentID
        self.ChildID
        self.unk1
        self.unk2
class IKInfo(object):
    def IKInfo(self):
        self.Unk0
        self.NextSectionEntryCount # idk what to call this
        self.Target
        self.Float
        self.Unk2
        self.Unk3
        self.NextDat
       
class VertexSet(object):
    def VertexSet(self):
        self.unk0
        self.unk1
        self.VtxCount
        self.unk2
        self.unk3
        self.unk4
        self.Vertices
        
class Vertex(object):
    def Vertex(self):
        self.Pos
        self.NormalDir
        self.UVCoord
        self.VertexColor
        self.Bone0
        self.Bone1
        self.Bone2
        self.Bone3
        self.Weight0
        self.Weight1
        self.Weight2
        self.Weight3
        self.VertID
        
class FaceSet(object):
    def FaceSet(self):
        self.unk0
        self.Idx
        self.FaceCount
        self.unk1
        self.FaceUnk
        self.unk2
        self.MatID
        self.unk3
        self.unk4
        self.FaceIndices
        self.FaceUnks
class Morph(object):
    def Morph(self):
        self.Name
        self.Panel
        self.VertCount
        self.VertTranslations
        
def ModelReader(f):
    f.seek(0x74)
    modelPhysicsNum = struct.unpack("I", f.read(4))[0]
    f.seek(0x94)
    TextureCount = struct.unpack('I', f.read(4))[0]
    f.seek(16, 1)
    TexNames = []
    for i in range(TextureCount):
        TexNames.append(f.read(32).split(b'\x00')[0].decode('ASCII'))
    MatCount = struct.unpack('I', f.read(4))[0]
    f.seek(16, 1)
    Materials = []
    for i in range(MatCount):
        Mat = Material()
        Mat.s1 = struct.unpack('I', f.read(4))[0]
        Mat.s2 = struct.unpack('h', f.read(2))[0]
        Mat.TexName = TexNames[struct.unpack('h', f.read(2))[0]]
        Mat.Diffuse = struct.unpack('BBBB', f.read(4))
        Mat.Ambient = struct.unpack('BBBB', f.read(4))
        Mat.Specular = struct.unpack('BBBB', f.read(4))
        Materials.append(Mat.__dict__)
    BoneCount = struct.unpack('I', f.read(4))[0]
    f.seek(16, 1)
    Bones = []
    for i in range(BoneCount):
        B = Bone()
        B.Name = f.read(32).split(b'\x00')[0].decode('Shift-JIS')
        B.BoneMatrix = [list(struct.unpack('ffff', f.read(16))), list(struct.unpack('ffff', f.read(16))), list(struct.unpack('ffff', f.read(16))), list(struct.unpack('ffff', f.read(16)))]
        B.BonePosition = list(struct.unpack('ffff', f.read(16)))
        if f.name == 'TEST.BMD':
            B.ParentID = struct.unpack('h', f.read(2))[0]
            B.ChildID = struct.unpack('h', f.read(2))[0]
            B.unk0 = struct.unpack('I', f.read(4))[0]
        else:
            B.unk0 = struct.unpack('I', f.read(4))[0]
            B.ParentID = struct.unpack('h', f.read(2))[0]
            B.ChildID = struct.unpack('h', f.read(2))[0]
        B.unk1 = struct.unpack('I', f.read(4))[0]
        B.unk2 = struct.unpack('I', f.read(4))[0]
        Bones.append(B.__dict__)
    IKInfoCount = struct.unpack('I', f.read(4))[0]
    f.seek(12, 1)
    IKInfos = []
    IKNextCount = 0
    for i in range(IKInfoCount):
        inf = IKInfo()
        inf.Unk0 = struct.unpack('I', f.read(4))[0]
        inf.NextSectionEntryCount = struct.unpack('H', f.read(2))[0] # idk what to call this
        IKNextCount += inf.NextSectionEntryCount
        inf.Target = struct.unpack('H', f.read(2))[0]
        inf.Float = struct.unpack('f', f.read(4))[0]
        inf.Unk2 = struct.unpack('H', f.read(2))[0]
        inf.Unk3 = struct.unpack('H', f.read(2))[0]
        inf.NextDat = []
        IKInfos.append(inf.__dict__)
    AfterIKUnk = struct.unpack('I', f.read(4))[0]
    for i in range(IKInfoCount):
        for a in range(IKInfos[i]["NextSectionEntryCount"]):
            IKInfos[i]["NextDat"].append(struct.unpack('H', f.read(2))[0])
    VertexSetCount = struct.unpack('I', f.read(4))[0]
    VertexSetList = []
    for i in range(VertexSetCount):
        V = VertexSet()
        V.unk0 = struct.unpack('I', f.read(4))[0]
        V.unk1 = struct.unpack('h', f.read(2))[0]
        V.VtxCount = struct.unpack('h', f.read(2))[0]
        V.unk2 = struct.unpack('I', f.read(4))[0]
        V.unk3 = struct.unpack('I', f.read(4))[0]
        V.unk4 = struct.unpack('I', f.read(4))[0]
        V.Vertices = []
        VertexSetList.append(V.__dict__)
    f.seek(4, 1)
    for i in range(len(VertexSetList)):
        for v in range(VertexSetList[i]["VtxCount"]):
            Vert = Vertex()
            Vert.Pos = list(struct.unpack('fff', f.read(12)))
            Vert.NormalDir = list(struct.unpack('fff', f.read(12)))
            Vert.UVCoord = list(struct.unpack('ff', f.read(8)))
            Vert.VertexColor = list(struct.unpack('BBBB', f.read(4)))
            Vert.Bone0 = struct.unpack('b', f.read(1))[0]
            Vert.Bone1 = struct.unpack('b', f.read(1))[0]
            Vert.Bone2 = struct.unpack('b', f.read(1))[0]
            Vert.Bone3 = struct.unpack('b', f.read(1))[0]
            Vert.Weight0 = struct.unpack('f', f.read(4))[0]
            Vert.Weight1 = struct.unpack('f', f.read(4))[0]
            Vert.Weight2 = struct.unpack('f', f.read(4))[0]
            Vert.Weight3 = struct.unpack('f', f.read(4))[0]
            Vert.VertID = struct.unpack('I', f.read(4))[0]
            VertexSetList[i]["Vertices"].append(Vert.__dict__)
    FaceSetCount = struct.unpack('I', f.read(4))[0]
    FaceSetList = []
    for i in range(FaceSetCount):
        Fc = FaceSet()
        Fc.unk0 = struct.unpack('I', f.read(4))[0]
        Fc.Idx = struct.unpack('I', f.read(4))[0]
        Fc.FaceCount = struct.unpack('h', f.read(2))[0]
        Fc.unk1 = struct.unpack('h', f.read(2))[0]
        Fc.FaceBoneCount = struct.unpack('h', f.read(2))[0]
        Fc.unk2 = struct.unpack('h', f.read(2))[0]
        Fc.MatID = struct.unpack('h', f.read(2))[0]
        Fc.unk3 = struct.unpack('h', f.read(2))[0]
        Fc.unk4 = struct.unpack('I', f.read(4))[0]
        Fc.FaceIndices = []
        Fc.FaceBones = []
        FaceSetList.append(Fc.__dict__)
    f.seek(4, 1)
    for i in range(FaceSetCount):
        for Fc in range(FaceSetList[i]["FaceCount"]):
            FaceSetList[i]["FaceIndices"].append(struct.unpack('H', f.read(2))[0])
        for Fu in range(FaceSetList[i]["FaceBoneCount"]):
            FaceSetList[i]["FaceBones"].append(struct.unpack('H', f.read(2))[0])
    MorphCount = struct.unpack('I', f.read(4))[0]
    f.seek(12, 1)
    Morphs = []
    for i in range(MorphCount):
        M = Morph()
        unk = f.read(4)
        M.Name = f.read(32).split(b'\x00')[0].decode('Shift-JIS')
        M.Panel = struct.unpack('I', f.read(4))[0]
        M.VertCount = struct.unpack('I', f.read(4))[0]
        M.VertTranslations = []
        Morphs.append(M.__dict__)
    f.seek(4, 1)
    # Second pass to gain the vert translations
    for i in range(MorphCount):
        for v in range(Morphs[i]["VertCount"]):
            Morphs[i]["VertTranslations"].append(list(struct.unpack('Ifff', f.read(16)))) # grabs the translation + vert index in one go
    return {"B3DModel": {"PhysicsNumber": modelPhysicsNum, "Textures": TexNames, "Materials": Materials, "Bones": Bones, "VertexSets": VertexSetList, "FaceSets": FaceSetList, "MorphData": Morphs}}
    
    
        
        
        
def AnimationHeadReader(f):
    AH = ANMHead()
    AH.magic = f.read(8)
    AH.unk01 = f.read(4)
    AH.unk02 = f.read(4)
    AH.unk03 = f.read(4)
    AH.HasMTN = struct.unpack('I', f.read(4))[0]
    AH.HasSKN = struct.unpack('I', f.read(4))[0]
    AH.unk06 = f.read(4)
    return AH
        
def MotionHeadReader(f):
    MH = MTNHead()
    MH.magic = f.read(8)
    MH.unk01 = f.read(4)
    MH.unk02 = f.read(4)
    MH.unk03 = f.read(4)
    MH.unk04 = f.read(4)
    MH.BoneCount = struct.unpack('I', f.read(4))[0]
    MH.unk05 = f.read(4)
    return MH
        
def SkinHeadReader(f):
    SH = SKNHead()
    SH.magic = f.read(8)
    SH.unk01 = f.read(4)
    SH.unk02 = f.read(4)
    SH.unk03 = f.read(4)
    SH.MorphCount = struct.unpack('I', f.read(4))[0]
    SH.unk04 = f.read(4)
    SH.unk05 = f.read(4)
    return SH
    
def BoneDataReader(f, BoneCount):
    BD = []
    for i in range(0, BoneCount):
        Bone = MTNBoneDef()
        Bone.Name = f.read(32)
        Bone.FrameCount = struct.unpack('I', f.read(4))[0]
        Bone.Index = struct.unpack('I', f.read(4))[0]
        Bone.unk01 = f.read(4)
        Bone.Type = struct.unpack('I', f.read(4))[0]
        Bone.Hash01 = f.read(4)
        Bone.hash02 = f.read(4)
        
        BD.append(Bone)
    return BD
    
def ConvertMotionToVMD(f, v):
    v.write(b'Vocaloid Motion Data 0002\x00\x00\x00\x00\x00')
    v.write(b'Megpoid the Music\x00\x00\x00')
    AH = AnimationHeadReader(f)
    if AH.HasMTN == 1:
        MH = MotionHeadReader(f)
        Bones = BoneDataReader(f, MH.BoneCount)
        bone_str = b''
        total_bone_frames = 0
        cur_bone = 0  # for debugging
        parsed = 0  # for center rotation if i ever implement it
        for Bone in Bones:
            print(Bone.Name.split(b'\x00')[0].decode('Shift-JIS'))
            temp = b''
            if Bone.Type == 3:
                for i in range(0, Bone.FrameCount):
                    temp += Bone.Name[0:15]
                    temp += struct.pack('I', int(i))
                    temp += f.read(12)
                    f.seek(4, 1)
                    parsed += 1
                    f.seek(16 * (Bone.FrameCount), 1)
                    temp += f.read(16)
                    f.seek(((16 * (Bone.FrameCount)) + 16) * -1, 1)
                    temp += dummy_interpolation
                f.seek(16 * Bone.FrameCount, 1)  # Apparently there's unused CENTER rotation?
                    
            elif Bone.Type == 2:
                for i in range(0, Bone.FrameCount):
                    temp += Bone.Name[0:15]
                    temp += struct.pack('I', i)
                    temp += dummy_position
                    temp += f.read(16)
                    temp += dummy_interpolation
            total_bone_frames += Bone.FrameCount
            bone_str += temp
            cur_bone += 1
        v.write(struct.pack('I', total_bone_frames))
        v.write(bone_str)
    if AH.HasSKN == 1:
        SH = SkinHeadReader(f)
        Morphs = []
        morph_str = b''
        morph_frames = 0
        for i in range(0, SH.MorphCount):
            morph = MorphDef()
            morph.Name = f.read(16)
            morph.Index = struct.unpack('I', f.read(4))[0]
            morph.FrameCount = struct.unpack('I', f.read(4))[0]
            morph.unk01 = f.read(4)
            morph.unk02 = f.read(4)
            Morphs.append(morph)
        for morph in Morphs:
            morph_frames += morph.FrameCount
            temp = b''
            for i in range(0, morph.FrameCount):
                temp += morph.Name[0:15]
                temp += f.read(4)
                temp += f.read(4)
                f.seek(8, 1)
            morph_str += temp
        v.write(struct.pack('I', morph_frames))
        v.write(morph_str)
            
        