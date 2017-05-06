#!/usr/bin/python
import random
import bpy
from bpy.types import Operator  
from bpy.props import FloatVectorProperty, FloatProperty, IntProperty 

bl_info = {
    "name": "UVTileRandom",
    "category": "Object",
}



#tx = 2
#ty = 2
#sx = 1.0 / tx
#sy = 1.0 / ty


class UVTileRandom(bpy.types.Operator):
    """UV Random Tile Layout"""
    bl_idname = "object.uvtilerandom"
    bl_label = "UV Tile Random"
    bl_options = {'REGISTER', 'UNDO'}

    tilesx = IntProperty(  
        name="Horizontal Tiles",  
        default=4,  
        subtype='FACTOR',  
        description="tilesx"  
        )

    tilesy = IntProperty(  
        name="Vertical Tiles",  
        default=4,  
        subtype='FACTOR',  
        description="tilesy"  
        )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):

        if bpy.context.scene.objects.active is None:
            print("No object is selected")
        else:
            tx = self.tilesx
            ty = self.tilesy
            sx = 1.0 / tx
            sy = 1.0 / ty

            bpy.ops.object.mode_set(mode='OBJECT')
            objname = bpy.context.scene.objects.active.name
            print("Selected object is " + objname)
            objref = bpy.data.objects[objname]
            mesh = objref.data
            bpy.ops.mesh.uv_texture_remove()
            print("Removed UV's")
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.editmode_toggle()
            bpy.ops.uv.reset()
            print("Created new UV's")
            bpy.ops.object.mode_set(mode='OBJECT')
            uvmap =mesh.uv_layers.active      
            print(uvmap)
            for f in mesh.polygons:
                print("Iterating ...")
                ix = random.randint(0, tx-1)
                iy = random.randint(0, ty-1)
                for i in f.loop_indices:
                    l = mesh.loops[i]
                    v = mesh.vertices[l.vertex_index]
                    for j, ul in enumerate(mesh.uv_layers):
                        print("Updating...")
                        uv = ul.data[l.index].uv
                        if uv.x == 1:
                            uv.x = sx
                        if uv.y == 1:
                            uv.y = sy
                        uv.x += (ix * sx)
                        uv.y += (iy * sy)
    
            return {'FINISHED'} 

def register():
    print("+++ UVTileRandomRegister()")
    bpy.utils.register_class(UVTileRandom)
def unregister():
    print("+++ UVTileRandomUnregister()")
    bpy.utils.unregister_class(UVTileRandom)

if __name__ == "__main__":
    register()
