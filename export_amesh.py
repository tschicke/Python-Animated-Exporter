import bpy

def save(operator, context, filepath=""):
    bpy.ops.object.mode_set(mode='OBJECT')
    
    vertices = []
    UVs = []
    normals = []
    boneIndices = []
    boneWeights = []
    
    skeletonArray = []
    
    indices = []
    
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
                    weight1 = 1
                    weight2 = 0
                    index1 = vert.groups[0].group
                    index2 = 0
                elif len(vert.groups) == 2:
                    weight1 = vert.groups[0].weight
                    weight2 = vert.groups[1].weight
                    divideBy = weight1 + weight2
                    if divideBy != 0:
                        weight1 /= divideBy
                        weight2 /= divideBy
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
                    divideBy = weight1 + weight2
                    if divideBy != 0:
                        weight1 /= divideBy
                        weight2 /= divideBy
                tempBoneIndices.append((index1, index2))
                tempBoneWeights.append((weight1, weight2))
            
            indexOffset = 0
            for face in mesh.tessfaces:
                tempIndices = []
                for i in range(0, len(face.vertices)):
                    index = face.vertices[i]
                    blenderVertex = mesh.vertices[index].co[:]
                    outVertex = (blenderVertex[0], blenderVertex[2], blenderVertex[1])
                    UV = mesh.tessface_uv_textures.active.data[face.index].uv[i][:]
                    if face.use_smooth:
                        normal = mesh.vertices[index].normal[:]
                    else:
                        normal = face.normal[:]
                    boneIndex = tempBoneIndices[index]
                    boneWeight = tempBoneWeights[index]
                    
                    dupIndex = -1
                    for j in range(0, len(vertices)):
                        tempVert = vertices[j]
                        tempUV = UVs[j]
                        tempNormal = normals[j]
                        tempBoneIndex = boneIndices[j]
                        tempBoneWeight = boneWeights[j]
                        
                        if outVertex == tempVert and UV == tempUV and normal == tempNormal and boneIndex == tempBoneIndex and boneWeight == tempBoneWeight:
                            #Duplicate Found
                            dupIndex = j
                            break
                    if dupIndex != -1:
                        #Duplicate Found
                        tempIndices.append(dupIndex)
                    else:
                        vertices.append(outVertex)
                        UVs.append(UV)
                        normals.append(normal)
                        boneIndices.append(boneIndex)
                        boneWeights.append(boneWeight)
                        tempIndices.append(indexOffset)
                        indexOffset += 1
                    
                if len(tempIndices) == 4:
                    indices.append((tempIndices[0], tempIndices[3], tempIndices[2]))
                    indices.append((tempIndices[0], tempIndices[2], tempIndices[1]))
                else:
                    indices.append((tempIndices[0], tempIndices[2], tempIndices[1]))
        elif object.type == "ARMATURE":
            armature = object.data
        
        file = open(filepath, 'w')
        fw = file.write
        fw("amdl\n")
        fw("%i %i\n" % (len(vertices), len(indices) * 3))
        
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
        
        file.close
    
    return {'FINISHED'}