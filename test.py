import os
clear = lambda: os.system('cls')


import bpy

mesh = bpy.data.objects['Cylinder'].data
skeleton = bpy.data.objects['TestArmature'].data

def printFunc():
    bpy.ops.object.mode_set(mode='OBJECT')
    clear()
    mesh.calc_tessface()

    print(dir(skeleton.bones[0]))
    
    for i in range(0, len(skeleton.bones)):
        bone = skeleton.bones[i]
        print()
        print("%.2f %.2f %.2f" % (bone.tail[:]))
        print("%.2f %.2f %.2f" % (bone.tail_local[:]))
        print("%.2f %.2f %.2f" % (bone.head[:]))
        print("%.2f %.2f %.2f" % (bone.head_local[:]))
        print(i, bone.name)
        if bone.parent == None:
            print("None")
        else:
            print(bone.parent.name)
    
printFunc()