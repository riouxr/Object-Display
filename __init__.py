bl_info = {
    "name": "Display Modes — Selected / Unselected / All",
    "author": "ChatGPT + User",
    "version": (1, 3, 1),
    "blender": (3, 0, 0),
    "location": "3D Viewport > Sidebar > View",
    "description": "Icon-only controls to set object display modes for Selected, Unselected, or All mesh objects",
    "category": "3D View",
}

import bpy

# -----------------------------
# Utilities (STRICT selection semantics)
# -----------------------------

def iter_selected_meshes(context):
    """Yield ONLY mesh objects that are currently selected in the viewport."""
    for obj in context.selected_objects:
        if obj and obj.type == 'MESH':
            yield obj

def iter_unselected_meshes(context):
    """Yield ONLY mesh objects in the scene that are NOT selected."""
    selected_set = {o for o in context.selected_objects if o and o.type == 'MESH'}
    for obj in context.scene.objects:
        if obj.type == 'MESH' and obj not in selected_set:
            yield obj

def _set_display_type(objs, display_type):
    for obj in objs:
        try:
            obj.display_type = display_type
        except Exception:
            pass

# -----------------------------
# Operators — ALL
# -----------------------------

class MESH_OT_display_bounds_all(bpy.types.Operator):
    bl_idname = "mesh.display_bounds_all"
    bl_label = "All Bounds"
    bl_description = "Set the display type of all meshes in the scene to Bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type((o for o in context.scene.objects if o.type == 'MESH'), 'BOUNDS')
        return {'FINISHED'}

class MESH_OT_display_wire_all(bpy.types.Operator):
    bl_idname = "mesh.display_wire_all"
    bl_label = "All Wire"
    bl_description = "Set the display type of all meshes in the scene to Wire"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type((o for o in context.scene.objects if o.type == 'MESH'), 'WIRE')
        return {'FINISHED'}

class MESH_OT_display_solid_all(bpy.types.Operator):
    bl_idname = "mesh.display_solid_all"
    bl_label = "All Solid"
    bl_description = "Set the display type of all meshes in the scene to Solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type((o for o in context.scene.objects if o.type == 'MESH'), 'SOLID')
        return {'FINISHED'}

class MESH_OT_display_texture_all(bpy.types.Operator):
    bl_idname = "mesh.display_texture_all"
    bl_label = "All Textured"
    bl_description = "Set the display type of all meshes in the scene to Textured"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type((o for o in context.scene.objects if o.type == 'MESH'), 'TEXTURED')
        return {'FINISHED'}

# -----------------------------
# Operators — SELECTED (STRICT)
# -----------------------------

class MESH_OT_display_bounds_selected(bpy.types.Operator):
    bl_idname = "mesh.display_bounds_selected"
    bl_label = "Selected Bounds"
    bl_description = "Set the display type of SELECTED mesh objects only to Bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(iter_selected_meshes(context), 'BOUNDS')
        return {'FINISHED'}

class MESH_OT_display_wire_selected(bpy.types.Operator):
    bl_idname = "mesh.display_wire_selected"
    bl_label = "Selected Wire"
    bl_description = "Set the display type of SELECTED mesh objects only to Wire"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(iter_selected_meshes(context), 'WIRE')
        return {'FINISHED'}

class MESH_OT_display_solid_selected(bpy.types.Operator):
    bl_idname = "mesh.display_solid_selected"
    bl_label = "Selected Solid"
    bl_description = "Set the display type of SELECTED mesh objects only to Solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(iter_selected_meshes(context), 'SOLID')
        return {'FINISHED'}

class MESH_OT_display_texture_selected(bpy.types.Operator):
    bl_idname = "mesh.display_texture_selected"
    bl_label = "Selected Textured"
    bl_description = "Set the display type of SELECTED mesh objects only to Textured"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(iter_selected_meshes(context), 'TEXTURED')
        return {'FINISHED'}

# -----------------------------
# Operators — UNSELECTED (STRICT)
# -----------------------------

class MESH_OT_display_bounds_unselected(bpy.types.Operator):
    bl_idname = "mesh.display_bounds_unselected"
    bl_label = "Unselected Bounds"
    bl_description = "Set the display type of UNSELECTED mesh objects only to Bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(iter_unselected_meshes(context), 'BOUNDS')
        return {'FINISHED'}

class MESH_OT_display_wire_unselected(bpy.types.Operator):
    bl_idname = "mesh.display_wire_unselected"
    bl_label = "Unselected Wire"
    bl_description = "Set the display type of UNSELECTED mesh objects only to Wire"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(iter_unselected_meshes(context), 'WIRE')
        return {'FINISHED'}

class MESH_OT_display_solid_unselected(bpy.types.Operator):
    bl_idname = "mesh.display_solid_unselected"
    bl_label = "Unselected Solid"
    bl_description = "Set the display type of UNSELECTED mesh objects only to Solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(iter_unselected_meshes(context), 'SOLID')
        return {'FINISHED'}

class MESH_OT_display_texture_unselected(bpy.types.Operator):
    bl_idname = "mesh.display_texture_unselected"
    bl_label = "Unselected Textured"
    bl_description = "Set the display type of UNSELECTED mesh objects only to Textured"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(iter_unselected_meshes(context), 'TEXTURED')
        return {'FINISHED'}

# -----------------------------
# Panel
# -----------------------------

class VIEW3D_PT_display(bpy.types.Panel):
    bl_label = "Display Modes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "View"

    def draw(self, context):
        layout = self.layout

        # --- Selected ---
        col = layout.column(align=True)
        col.label(text="Selected")
        row = col.row(align=True)
        row.operator("mesh.display_bounds_selected", text="", icon="PIVOT_BOUNDBOX")
        row.operator("mesh.display_wire_selected",   text="", icon="MOD_WIREFRAME")
        row.operator("mesh.display_solid_selected",  text="", icon="SHADING_SOLID")
        row.operator("mesh.display_texture_selected",text="", icon="TEXTURE")

        # --- Unselected ---
        col = layout.column(align=True)
        col.separator()
        col.label(text="Unselected")
        row = col.row(align=True)
        row.operator("mesh.display_bounds_unselected", text="", icon="PIVOT_BOUNDBOX")
        row.operator("mesh.display_wire_unselected",   text="", icon="MOD_WIREFRAME")
        row.operator("mesh.display_solid_unselected",  text="", icon="SHADING_SOLID")
        row.operator("mesh.display_texture_unselected",text="", icon="TEXTURE")

        # --- All ---
        col = layout.column(align=True)
        col.separator()
        col.label(text="All")
        row = col.row(align=True)
        row.operator("mesh.display_bounds_all", text="", icon="PIVOT_BOUNDBOX")
        row.operator("mesh.display_wire_all",   text="", icon="MOD_WIREFRAME")
        row.operator("mesh.display_solid_all",  text="", icon="SHADING_SOLID")
        row.operator("mesh.display_texture_all",text="", icon="TEXTURE")

# -----------------------------
# Registration
# -----------------------------

classes = (
    # Panel
    VIEW3D_PT_display,

    # All
    MESH_OT_display_bounds_all,
    MESH_OT_display_wire_all,
    MESH_OT_display_solid_all,
    MESH_OT_display_texture_all,

    # Selected
    MESH_OT_display_bounds_selected,
    MESH_OT_display_wire_selected,
    MESH_OT_display_solid_selected,
    MESH_OT_display_texture_selected,

    # Unselected
    MESH_OT_display_bounds_unselected,
    MESH_OT_display_wire_unselected,
    MESH_OT_display_solid_unselected,
    MESH_OT_display_texture_unselected,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
