import os


def clear():
    #os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(0, 30):
        print()


import bpy

mesh = bpy.data.objects['Cylinder'].data
skeleton = bpy.data.objects['Armature'].data

def printFunc():
    bpy.ops.object.mode_set(mode='OBJECT')
    clear()
    mesh.calc_tessface()
    
    for bone in skeleton.bones:
        print(bone.name)

printFunc()