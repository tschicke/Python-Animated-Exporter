bl_info = {
    "name":         "OGL Lib Animated Mesh Format",
    "author":       "Tyler Schicke",
    "blender":      (2, 6, 2),
    "version":      (0, 0, 1),
    "location":     "File > Import-Export",
    "description":  "Export Animated Meshes for OGL Lib",
    "category":     "Import-Export"
}

if "bpy" in locals():
    import imp;
    if "export_amesh" in locals():
        imp.reload(export_amesh);

import bpy
from bpy_extras.io_utils import ExportHelper

class OGLExporter(bpy.types.Operator, ExportHelper):
    bl_idname       = "export_amesh.amesh"
    bl_label        = "OGL Animated Exporter"
    bl_options      = {'PRESET'}
    
    filename_ext    = ".amesh"
    
    def execute(self, context):
        from . import export_amesh
        
        return export_amesh.save(self, context, self.filepath)
        
def menu_func(self, context):
    self.layout.operator(OGLExporter.bl_idname, text="OGL Animated Mesh Format (.amesh)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()