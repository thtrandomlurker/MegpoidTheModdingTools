# make all selected objects use unique mats
import bpy

for obj in bpy.context.selected_objects:
    if obj.select:
        print(obj.name)
        mat = obj.active_material
        if mat:
            obj.active_material = mat.copy()
            obj.active_material.name = "mat_" + obj.name