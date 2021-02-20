import random
import bpy
from bpy.types import Operator  
from bpy.props import FloatVectorProperty, FloatProperty, IntProperty 

bl_info = {
    "name": "UV Tile Random",
    "author": "Dan Morriss",
    "version": (1, 1, 1),
    "blender": (2, 80, 0),
    "location": "Image-Window > UV > UV Tile Random",
    "description": "Tile UV's Randomly",
    "warning": "",
    "doc_url": "{BLENDER_MANUAL_URL}/addons/import_export/mesh_uv_layout.html",
    "support": 'OFFICIAL',
    "category": "UV",
}


from bpy.props import (
    IntProperty,
)


#tx = 2
#ty = 2
#sx = 1.0 / tx
#sy = 1.0 / ty


class UVTileRandom(bpy.types.Operator):
    """Randomly Tile UV's"""
    bl_idname = "uv.tile_random"
    bl_label = "Random Tile UV's"
    bl_options = {'REGISTER', 'UNDO'}

    tilesx: IntProperty(  
        name="Horizontal Tiles",  
        default=4,  
        subtype='FACTOR',  
        description="tilesx"  
        )

    tilesy: IntProperty(  
        name="Vertical Tiles",  
        default=4,  
        subtype='FACTOR',  
        description="tilesy"  
        )

    
    def invoke(self, context, event):
        print("UVTileRandom::Invoke")
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        print("UVTileRandom::Execute")
        obj = bpy.context.active_object
        #obj = bpy.context.window.scene.objects[0]
        if obj is None:
        #if bpy.context.scene.objects.active is None:
            print("No object is selected")
        else:
            tx = self.tilesx
            ty = self.tilesy
            sx = 1.0 / tx
            sy = 1.0 / ty

            bpy.ops.object.mode_set(mode='OBJECT')
            # objname = bpy.context.scene.objects.active.name
            objname = obj.name
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
                #print("Iterating ...")
                ix = random.randint(0, tx-1)
                iy = random.randint(0, ty-1)
                for i in f.loop_indices:
                    l = mesh.loops[i]
                    v = mesh.vertices[l.vertex_index]
                    for j, ul in enumerate(mesh.uv_layers):
                        #print("Updating...")
                        uv = ul.data[l.index].uv
                        if uv.x == 1:
                            uv.x = sx
                        if uv.y == 1:
                            uv.y = sy
                        uv.x += (ix * sx)
                        uv.y += (iy * sy)
    
            return {'FINISHED'} 

classes = (
    UVTileRandom,
)

def menu_func(self, context):
    self.layout.operator(UVTileRandom.bl_idname)


def register():
    from bpy.utils import register_class
    print("+++ UVTileRandomRegister()")
    for cls in classes:
        register_class(cls)
        bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    print("+++ UVTileRandomUnregister()")
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()
