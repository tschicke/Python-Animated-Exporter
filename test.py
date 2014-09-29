import os


def clear():
    #os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(0, 30):
        print()


import bpy

mesh = bpy.data.objects['Cube'].data
skeleton = bpy.data.objects['Armature'].data

def printFunc():
    bpy.ops.object.mode_set(mode='OBJECT')
    clear()
    mesh.calc_tessface()
    
    file = open("C:\\Users\\Tyler\\AppData\\Roaming\\Blender Foundation\\Blender\\2.70\\scripts\\addons\\io_mesh_animated\\test.txt", 'w')
    fw = file.write
    
    for vertex in mesh.vertices:
        print("Coord ", vertex.co[0])
        for group in vertex.groups:
            print("Tail Local ", skeleton.bones[group.group].tail_local[0])
            
    for i in range(0, len(skeleton.bones)):
        bone = skeleton.bones[i]
        fw("%i\n" % i)
        fw(bone.name + "\n")
        fw("head       %f %f %f\n" % bone.head[:])
        fw("head local %f %f %f\n" % bone.head_local[:])
        fw("tail       %f %f %f\n" % bone.tail[:])
        fw("tail local %f %f %f\n" % bone.tail_local[:])
    
    file.close()
    

printFunc()