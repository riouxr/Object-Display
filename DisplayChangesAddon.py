bl_info = {
    "name": "Mesh Display",
    "description": "Adds buttons to quickly switch between mesh display types.",
    "author": "Blender Bob, Chat GPT",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Tool > Display",
    "category": "Mesh",
    "support": "COMMUNITY"       
}

import bpy


class VIEW3D_PT_display(bpy.types.Panel):
    bl_label = "Display"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("mesh.display_texture_selected", text="Textured")
        row = layout.row()
        #row.operator("mesh.display_solid_selected", text="Solid")
        #row = layout.row()
        row.operator("mesh.display_wire_selected", text="Wire")
        row = layout.row()
        row.operator("mesh.display_bounds_selected", text="Bounds")        

        layout.separator()

        row = layout.row()
        row.operator("mesh.display_texture_all", text="All Textured")
        row = layout.row()
        #row.operator("mesh.display_solid_all", text="All Solid")
        #row = layout.row()
        row.operator("mesh.display_wire_all", text="All Wire")
        row = layout.row()
        row.operator("mesh.display_bounds_all", text="All Bounds")


class MESH_OT_display_bounds_all(bpy.types.Operator):
    bl_idname = "mesh.display_bounds_all"
    bl_label = "All Bounds"
    bl_description = "Set the display type of all mesh in the scene to bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.display_type = 'BOUNDS'
        return {'FINISHED'}


class MESH_OT_display_texture_all(bpy.types.Operator):
    bl_idname = "mesh.display_texture_all"
    bl_label = "All Textured"
    bl_description = "Set the display type of all mesh in the scene to texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.display_type = 'TEXTURED'
        return {'FINISHED'}


class MESH_OT_display_wire_all(bpy.types.Operator):
    bl_idname = "mesh.display_wire_all"
    bl_label = "All Wire"
    bl_description = "Set the display type of all mesh in the scene to wire"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.display_type = 'WIRE'
        return {'FINISHED'}


class MESH_OT_display_solid_all(bpy.types.Operator):
    bl_idname = "mesh.display_solid_all"
    bl_label = "All Solid"
    bl_description = "Set the display type of all mesh in the scene to solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.display_type = 'SOLID'
        return {'FINISHED'}


class MESH_OT_display_bounds_selected(bpy.types.Operator):
    bl_idname = "mesh.display_bounds_selected"
    bl_label = "Selected Bounds"
    bl_description = "Set the display type of selected mesh to bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.display_type = 'BOUNDS'
        return {'FINISHED'}

class MESH_OT_display_texture_selected(bpy.types.Operator):
    bl_idname = "mesh.display_texture_selected"
    bl_label = "Selected Textured"
    bl_description = "Set the display type of selected mesh to texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.display_type = 'TEXTURED'
        return {'FINISHED'}

class MESH_OT_display_wire_selected(bpy.types.Operator):
    bl_idname = "mesh.display_wire_selected"
    bl_label = "Selected Wire"
    bl_description = "Set the display type of selected mesh to wire"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.display_type = 'WIRE'
        return {'FINISHED'}    

class MESH_OT_display_solid_selected(bpy.types.Operator):
    bl_idname = "mesh.display_solid_selected"
    bl_label = "Selected Solid"
    bl_description = "Set the display type of selected mesh to solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                obj.display_type = 'SOLID'
        return {'FINISHED'}

classes = (
    VIEW3D_PT_display,
    MESH_OT_display_bounds_all,
    MESH_OT_display_texture_all,
    MESH_OT_display_wire_all,
    MESH_OT_display_solid_all,
    MESH_OT_display_bounds_selected,
    MESH_OT_display_texture_selected,
    MESH_OT_display_wire_selected,
    MESH_OT_display_solid_selected,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
