bl_info = {
    "name": "Sew Vertices",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import bgl
import gpu
import math
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from bpy_extras.view3d_utils import region_2d_to_location_3d, location_3d_to_region_2d
import bmesh

class SewVerticesOperator(bpy.types.Operator):
    bl_idname = "view3d.sew_vertices"
    bl_label = "Sew Vertices"
    bl_options = {'REGISTER'}

    def __init__(self):
        self.circle_pos = Vector((0, 0))
        self.radius = 30
        self.running = False
        self.selecting = False
        self._handle = None
        
    @classmethod
    def poll(cls, context):
        obj = context.object
        return (
            obj and obj.mode == 'EDIT' and 
            obj.type == 'MESH' and 
            context.tool_settings.mesh_select_mode[0]
        )

    def modal(self, context, event):
        if event.type in {'ESC'}:
            self.unregister_draw_handler()
            self.running = False
            context.area.tag_redraw()
            return {'FINISHED'}
        
        elif event.type in {'Z'} and event.ctrl:
            return {'PASS_THROUGH'}
        
        elif event.type == 'MIDDLEMOUSE' and event.value == 'PRESS':
            return {'PASS_THROUGH'}

        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self.selecting = True
            self.sew_vertices(context)
            return {'RUNNING_MODAL'}
        
        elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            bpy.ops.ed.undo_push(message="Vertices sewn")
            self.selecting = False
            self.finish(context)

        elif event.type == 'MOUSEMOVE':
            self.circle_pos = Vector((event.mouse_region_x, event.mouse_region_y))
            mesh = context.object.data
            bm = bmesh.from_edit_mesh(mesh)
            region = context.region
            rv3d = context.space_data.region_3d
            if self.selecting == True:
                self.sew_vertices(context)
            context.area.tag_redraw()
            return {'RUNNING_MODAL'}
        
        elif event.type == 'WHEELUPMOUSE':
            if event.shift:
                self.radius = min(500, self.radius + 5)
                context.area.tag_redraw()
                return {'RUNNING_MODAL'}
            return {'PASS_THROUGH'}

        elif event.type == 'WHEELDOWNMOUSE':
            if event.shift:
                self.radius = max(5, self.radius - 5)
                context.area.tag_redraw()
                return {'RUNNING_MODAL'}
            return {'PASS_THROUGH'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        if context.area.type == 'VIEW_3D':
            self.register_draw_handler(context)
            context.window_manager.modal_handler_add(self)
            self.running = True
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}

    def finish(self, context):
        context.area.tag_redraw()
        return {'FINISHED'}

    def draw_circle(self):
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        vertices = []
        segments = 32
        for i in range(segments):
            angle = 2 * 3.14159 * i / segments
            x = self.circle_pos.x + self.radius * math.cos(angle)
            y = self.circle_pos.y + self.radius * math.sin(angle)
            vertices.append((x, y))

        batch = batch_for_shader(shader, 'LINE_LOOP', {"pos": vertices})
        shader.bind()
        shader.uniform_float("color", (1.0, 0.5, 0.2, 1.0))
        batch.draw(shader)

    def draw_callback(self, context):
        if self.running:
            self.draw_circle()

    def register_draw_handler(self, context):
        self._handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')

    def unregister_draw_handler(self):
        if hasattr(self, "_handle"):
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            
    def sew_vertices(self, context):
        obj = context.object
        if obj and obj.type == 'MESH':
            mesh = obj.data
            bm = bmesh.from_edit_mesh(mesh)
            region = context.region
            rv3d = context.space_data.region_3d
            matrix_world = obj.matrix_world

            for vert in bm.verts:
                world_coord = matrix_world @ vert.co
                screen_coord = location_3d_to_region_2d(region, rv3d, world_coord)
                if screen_coord is None:
                    continue
                dist = (screen_coord - self.circle_pos).length
                vert.select = False
                if dist <= self.radius:
                    vert.select = True
            bpy.ops.mesh.merge(type='CENTER')
            for vert in bm.verts:
                vert.select = False

            bmesh.update_edit_mesh(mesh, loop_triangles=False, destructive=False)
            context.area.tag_redraw()

def draw_context_menu(self, context):
    layout = self.layout
    layout.operator("view3d.sew_vertices")
        
def register():
    bpy.utils.register_class(SewVerticesOperator)
    for f in bpy.types.VIEW3D_MT_edit_mesh_context_menu._dyn_ui_initialize():
        if f.__name__ == draw_context_menu.__name__:
            bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(f)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(draw_context_menu)
    
def unregister():
    bpy.utils.unregister_class(SewVerticesOperator)
    for f in bpy.types.VIEW3D_MT_edit_mesh_context_menu._dyn_ui_initialize():
        if f.__name__ == draw_context_menu.__name__:
            bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(f)

if __name__ == "__main__":
    register()
