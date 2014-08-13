import bpy

def save(operator, context, filepath=""):
    bpy.ops.object.mode_set(mode='OBJECT')
    
    vertices = []
    UVs = []
    normals = []
    boneIndices = []
    boneWeights = []
    
    skeletonData = []
    boneIndexLookup = []
    
    indices = []
    
    print("Exporting")
    
    for object in bpy.data.objects:
        if object.type == "ARMATURE":
            armature = object.data
            
            startNodes = []
            
            for i in range(0, len(armature.bones)):
                bone = armature.bones[i]
                if bone.parent == None:
                    dupIndex = -1
                    for j in range(0, len(startNodes)):
                        if bone.head[:] == startNodes[j][:3]:
                            dupIndex = j
                            break
                    
                    if dupIndex == -1:    
                        baseNode = bone.head_local
                        index = i + len(startNodes)
                        parentIndex = -1
                        skeletonData.append((baseNode.x, baseNode.z, -baseNode.y, index, parentIndex))
                        startNodes.append((baseNode.x, baseNode.y, baseNode.z, index, parentIndex))
                        parentIndex = index
                        index += 1
                    else:
                        parentIndex = dupIndex
                        index = i + len(startNodes)
                        
                    tailOffset = bone.tail_local
                    skeletonData.append((tailOffset.x, tailOffset.z, -tailOffset.y, index, parentIndex))
                else:
                    offset = bone.tail_local
                    index = i + len(startNodes)
                    parentIndex = -1
                    for j in range(0, i):
                        if bone.parent == armature.bones[j]:
                            parentIndex = j + len(startNodes)
                            break
                    skeletonData.append((offset.x, offset.z, -offset.y, index, parentIndex))
                print(len(startNodes))
                boneIndexLookup.append(i + len(startNodes))
    
    for object in bpy.data.objects:
        if object.type == 'MESH':
            mesh = object.data
            mesh.calc_tessface()
            
            tempBoneIndices = []
            tempBoneWeights = []
            
            for vert in mesh.vertices:
                weight1 = 0
                weight2 = 0
                index1 = 0
                index2 = 0
                if len(vert.groups) == 0:
                    weight1 = 0
                    weight2 = 0
                    index1 = 0
                    index2 = 0
                elif len(vert.groups) == 1:
                    weight1 = 0 if vert.groups[0].weight < 0.001 else 1
                    weight2 = 0
                    index1 = vert.groups[0].group
                    index2 = 0
                elif len(vert.groups) == 2:
                    weight1 = vert.groups[0].weight
                    weight1 = 0 if weight1 < 0.001 else weight1
                    weight2 = vert.groups[1].weight
                    weight2 = 0 if weight2 < 0.001 else weight2
                    index1 = vert.groups[0].group
                    index2 = vert.groups[1].group
                else:
                    for group in vert.groups:
                        if weight1 > weight2:
                            if group.weight > weight2:
                                weight2 = group.weight
                                index2 = group.group
                        else:
                            if group.weight > weight1:
                                weight1 = group.weight
                                index1 = group.group
                    weight1 = 0 if weight1 < 0.001 else weight1
                    weight2 = 0 if weight2 < 0.001 else weight2
                    
                #Fix this so that deleting a bone won't shift indices
                if index1 >= len(boneIndexLookup):
                    index1 = 0
                    weight1 = 0
                if index2 >= len(boneIndexLookup):
                    index2 = 0
                    weight2 = 0
                divideBy = weight1 + weight2
                if divideBy != 0:
                    weight1 /= divideBy
                    weight2 /= divideBy
                tempBoneIndices.append((boneIndexLookup[index1], boneIndexLookup[index2]))
                tempBoneWeights.append((weight1, weight2))
            
            indexOffset = 0
            for face in mesh.tessfaces:
                tempIndices = []
                for i in range(0, len(face.vertices)):
                    index = face.vertices[i]
                    blenderVertex = mesh.vertices[index].co[:]
                    outVertex = (blenderVertex[0], blenderVertex[2], -blenderVertex[1])
                    UV = mesh.tessface_uv_textures.active.data[face.index].uv[i][:]
                    if face.use_smooth:
                        blenderNormal = mesh.vertices[index].normal[:]
                        outNormal = (blenderNormal[0], blenderNormal[2], -blenderNormal[1])
                    else:
                        blenderNormal = face.normal[:]
                        outNormal = (blenderNormal[0], blenderNormal[2], -blenderNormal[1])
                    boneIndex = tempBoneIndices[index]
                    boneWeight = tempBoneWeights[index]
                    
                    dupIndex = -1
                    for j in range(0, len(vertices)):
                        tempVert = vertices[j]
                        tempUV = UVs[j]
                        tempNormal = normals[j]
                        tempBoneIndex = boneIndices[j]
                        tempBoneWeight = boneWeights[j]
                        
                        if outVertex == tempVert and UV == tempUV and outNormal == tempNormal and boneIndex == tempBoneIndex and boneWeight == tempBoneWeight:
                            #Duplicate Found
                            dupIndex = j
                            break
                    if dupIndex != -1:
                        #Duplicate Found
                        tempIndices.append(dupIndex)
                    else:
                        vertices.append(outVertex)
                        UVs.append(UV)
                        normals.append(outNormal)
                        boneIndices.append(boneIndex)
                        boneWeights.append(boneWeight)
                        tempIndices.append(indexOffset)
                        indexOffset += 1
                    
                if len(tempIndices) == 4:
                    indices.append((tempIndices[0], tempIndices[1], tempIndices[2]))
                    indices.append((tempIndices[0], tempIndices[2], tempIndices[3]))
                else:
                    indices.append((tempIndices[0], tempIndices[1], tempIndices[2]))
        
        file = open(filepath, 'w')
        fw = file.write
        fw("amdl\n")
        fw("%i %i %i\n" % (len(vertices), len(indices) * 3, len(skeletonData)))
        
        for v in vertices:
            fw("v %f %f %f\n" % v[:])
        
        for uv in UVs:
            fw("t %f %f\n" % uv[:])
        
        for n in normals:
            fw("n %f %f %f\n" % n[:])
        
        for bi in boneIndices:
            fw("b %i %i\n" % bi[:])
            
        for bw in boneWeights:
            fw("w %f %f\n" % bw[:])
        
        for i in indices:
            fw("i %i %i %i\n" % i[:])
        
        for node in skeletonData:
            fw("s %f %f %f %i %i\n" % node[:])
        
        file.close
        
    print("Finished Exporting")
    
    return {'FINISHED'}