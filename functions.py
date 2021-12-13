import B3DLIB
import tkinter as tk
from tkinter import filedialog
import os
import json
import struct

def convBMM():
    root = tk.Tk().withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("BMM Motion File", "*.BMM")])
    ext = os.path.splitext(file_path)
    with open(file_path, 'rb') as inp:
        with open(ext[0] + '.vmd', 'wb') as outp:
            B3DLIB.ConvertMotionToVMD(inp, outp)
            
def convBMD(dumpJson=False):
    root = tk.Tk().withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("BMD Model File", "*.BMD")])
    ext = os.path.splitext(file_path)
    with open(file_path, 'rb') as bmd:
        MeshData = B3DLIB.ModelReader(bmd)
        if dumpJson:
            with open(file_path + '.json', 'w') as j:
                json.dump(MeshData, j, indent=2, ensure_ascii=False)
        # I'll do this in preprocessing, it's easier that way
        VertIDList = []
        for i in range(len(MeshData["B3DModel"]["FaceSets"])):
            AllowedBones = MeshData["B3DModel"]["FaceSets"][i]["FaceBones"]
            for v in range(len(MeshData["B3DModel"]["VertexSets"][i]["Vertices"])):
                try:
                    MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone0"] = AllowedBones[MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone0"]]
                except:
                    MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone0"] = MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone0"]
                try:
                    MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone1"] = AllowedBones[MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone1"]]
                except:
                    MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone1"] = MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone1"]
                try:
                    MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone2"] = AllowedBones[MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone2"]]
                except:
                    MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone2"] = MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone2"]
                try:
                    MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone3"] = AllowedBones[MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone3"]]
                except:
                    MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone4"] = MeshData["B3DModel"]["VertexSets"][i]["Vertices"][v]["Bone3"]
                
        with open(file_path[:-3] + 'pmx', 'wb') as pmx:
            pmx.write(b'PMX ')
            pmx.write(struct.pack('f', float(2)))
            pmx.write(b'\x08\x00\x00\x04\x04\x04\x04\x04\x04')
            pmx.write(b'\x16\x00\x00\x00' + str('OBJ_MIG.BMD').encode('UTF-16-LE'))
            pmx.write(b'\x16\x00\x00\x00' + str('OBJ_MIG.BMD').encode('UTF-16-LE'))
            pmx.write(b'\x16\x00\x00\x00' + str('OBJ_MIG.BMD').encode('UTF-16-LE'))
            pmx.write(b'\x16\x00\x00\x00' + str('OBJ_MIG.BMD').encode('UTF-16-LE'))
            VertCountOff = pmx.tell()
            VertCount = 0
            pmx.write(b'\x00\x00\x00\x00')
            for VSet in MeshData["B3DModel"]["VertexSets"]:
                HighestBone = 0
                for Vert in VSet["Vertices"]:
                    VertIDList.append(Vert["VertID"])
                    pmx.write(struct.pack('f', Vert["Pos"][0]))
                    pmx.write(struct.pack('f', Vert["Pos"][1]))
                    pmx.write(struct.pack('f', Vert["Pos"][2]))
                    pmx.write(struct.pack('f', Vert["NormalDir"][0]))
                    pmx.write(struct.pack('f', Vert["NormalDir"][1]))
                    pmx.write(struct.pack('f', Vert["NormalDir"][2]))
                    pmx.write(struct.pack('f', Vert["UVCoord"][0]))
                    pmx.write(struct.pack('f', Vert["UVCoord"][1]))
                    pmx.write(b'\x02')
                    pmx.write(struct.pack('i', Vert["Bone0"]))
                    pmx.write(struct.pack('i', Vert["Bone1"]))
                    pmx.write(struct.pack('i', Vert["Bone2"]))
                    pmx.write(struct.pack('i', Vert["Bone3"]))
                    pmx.write(struct.pack('f', Vert["Weight0"]))
                    pmx.write(struct.pack('f', Vert["Weight1"]))
                    pmx.write(struct.pack('f', Vert["Weight2"]))
                    pmx.write(struct.pack('f', Vert["Weight3"]))
                    pmx.write(struct.pack('f', float(1)))
                    VertCount += 1
            Cur = pmx.tell()
            pmx.seek(VertCountOff)
            pmx.write(struct.pack('I', VertCount))
            pmx.seek(Cur)
            FaceCountOff = pmx.tell()
            print(FaceCountOff)
            FaceCount = 0
            pmx.write(b'\x00\x00\x00\x00')
            VIndIncrement = 0
            for FS in range(len(MeshData["B3DModel"]["FaceSets"])):
                for i in range(MeshData["B3DModel"]["FaceSets"][FS]["FaceCount"]):
                    if i % 3 == 2:
                        pmx.write(struct.pack('I', MeshData["B3DModel"]["FaceSets"][FS]["FaceIndices"][i - 2] + VIndIncrement))
                        pmx.write(struct.pack('I', MeshData["B3DModel"]["FaceSets"][FS]["FaceIndices"][i - 1] + VIndIncrement))
                        pmx.write(struct.pack('I', MeshData["B3DModel"]["FaceSets"][FS]["FaceIndices"][i] + VIndIncrement))
                        FaceCount += 1
                VIndIncrement += MeshData["B3DModel"]["VertexSets"][FS]["VtxCount"]
            Cur = pmx.tell()
            pmx.seek(FaceCountOff)
            pmx.write(struct.pack('I', FaceCount * 3))
            pmx.seek(Cur)
            pmx.write(struct.pack('I', len(MeshData["B3DModel"]["Textures"])))
            for tex in MeshData["B3DModel"]["Textures"]:
                pmx.write(struct.pack('I', len(tex.encode('UTF-16-LE'))))
                pmx.write(tex.encode('UTF-16-LE'))
            pmx.write(struct.pack('I', len(MeshData["B3DModel"]["FaceSets"])))
            for i in range(len(MeshData["B3DModel"]["FaceSets"])):
                pmx.write(struct.pack('I', len(str(f'Material {i}').encode('UTF-16-LE'))))
                pmx.write(str(f'Material {i}').encode('UTF-16-LE'))
                pmx.write(struct.pack('I', len(str(f'Material {i}').encode('UTF-16-LE'))))
                pmx.write(str(f'Material {i}').encode('UTF-16-LE'))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Diffuse"][0] / 255))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Diffuse"][1] / 255))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Diffuse"][2] / 255))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Diffuse"][3] / 255))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Specular"][0] / 255))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Specular"][1] / 255))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Specular"][2] / 255))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Specular"][3] / 255))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Ambient"][0] / 255))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Ambient"][1] / 255))
                pmx.write(struct.pack('f', MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["Ambient"][2] / 255))
                pmx.write(b'\x0F')
                pmx.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
                pmx.write(struct.pack('I', MeshData["B3DModel"]["Textures"].index(MeshData["B3DModel"]["Materials"][MeshData["B3DModel"]["FaceSets"][i]["MatID"]]["TexName"])))
                pmx.write(b'\xFF\xFF\xFF\xFF')
                pmx.write(b'\x00\x00\xFF\xFF\xFF\xFF\x00\x00\x00\x00')
                pmx.write(struct.pack('I', MeshData["B3DModel"]["FaceSets"][i]["FaceCount"]))
            pmx.write(struct.pack('I', len(MeshData["B3DModel"]["Bones"])))
            for Bone in MeshData["B3DModel"]["Bones"]:
                print(Bone["Name"])
                pmx.write(struct.pack('I', len(Bone["Name"].encode('UTF-16-LE'))))
                pmx.write(Bone["Name"].encode('UTF-16-LE'))
                pmx.write(struct.pack('I', len(Bone["Name"].encode('UTF-16-LE'))))
                pmx.write(Bone["Name"].encode('UTF-16-LE'))
                pmx.write(struct.pack('f', Bone["BonePosition"][0]))
                pmx.write(struct.pack('f', Bone["BonePosition"][1]))
                pmx.write(struct.pack('f', Bone["BonePosition"][2]))
                pmx.write(struct.pack('i', Bone["ParentID"]))
                pmx.write(b'\x00\x00\x00\x00')
                pmx.write(b'\x0a\x00')
                pmx.write(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            pmx.write(struct.pack('i', len(MeshData["B3DModel"]["MorphData"]) - 1))
            for morph in MeshData["B3DModel"]["MorphData"]:
                if morph["Name"] == 'base':
                    print('Skipping Base Morph, Redundant for MMD')
                else:
                    pmx.write(struct.pack('I', len(morph["Name"].encode('UTF-16-LE'))))
                    pmx.write(morph["Name"].encode('UTF-16-LE'))
                    pmx.write(struct.pack('I', len(morph["Name"].encode('UTF-16-LE'))))
                    pmx.write(morph["Name"].encode('UTF-16-LE'))
                    pmx.write(struct.pack('b', morph["Panel"]))
                    pmx.write(b'\x01')
                    pmx.write(struct.pack('I', morph["VertCount"]))
                    for vert in morph["VertTranslations"]:
                        pmx.write(struct.pack('i', VertIDList.index(MeshData["B3DModel"]["MorphData"][0]["VertTranslations"][vert[0]][0])))
                        pmx.write(struct.pack('f', vert[1]))
                        pmx.write(struct.pack('f', vert[2]))
                        pmx.write(struct.pack('f', vert[3]))
            pmx.write(b'\x00\x00\x00\x00')
            print('I\'m here')
            pmx.write(b'\x00\x00\x00\x00')
            pmx.write(b'\x00\x00\x00\x00')
            pmx.write(b'\x00\x00\x00\x00')
        
