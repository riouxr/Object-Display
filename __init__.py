bl_info = {
    "name": "Display Modes — Selected / Unselected / All",
    "author": "ChatGPT + User",
    "version": (1, 3, 0),
    "blender": (3, 0, 0),
    "location": "3D Viewport > Sidebar > View",
    "description": "Icon-only controls to set object display modes for Selected, Unselected, or All mesh objects",
    "category": "3D View",
}

import bpy

# -----------------------------
# Utilities
# -----------------------------

def get_selected_meshes_and_collections(context):
    """
    Yield mesh objects that are either:
    - directly selected,
    - inside selected collection instances (empties instancing collections),
    - inside selected collections (including nested subcollections).
    """
    processed_objects = set()

    # Directly selected mesh objects and collection instances via empties
    for obj in context.selected_objects:
        if obj.type == 'MESH' and obj not in processed_objects:
            processed_objects.add(obj)
            yield obj
        elif obj.type == 'EMPTY' and obj.instance_type == 'COLLECTION' and obj.instance_collection:
            for inst_obj in obj.instance_collection.objects:
                if inst_obj.type == 'MESH' and inst_obj not in processed_objects:
                    processed_objects.add(inst_obj)
                    yield inst_obj

    # Selected collections (from Outliner) and active layer collection (viewport)
    def iter_meshes_in_collection(col, processed):
        for o in col.objects:
            if o.type == 'MESH' and o not in processed:
                processed.add(o)
                yield o
        for sub in col.children:
            yield from iter_meshes_in_collection(sub, processed)

    selected_collections = []
    # Some Blender builds expose selected IDs (e.g., Outliner selection)
    if hasattr(context, "selected_ids") and getattr(context, "selected_ids"):
        for item in context.selected_ids:
            try:
                if getattr(item, "bl_rna", None) and item.bl_rna.identifier == "Collection":
                    selected_collections.append(item)
            except Exception:
                pass

    active_col = context.view_layer.active_layer_collection.collection if context.view_layer and context.view_layer.active_layer_collection else None
    if active_col and active_col not in selected_collections:
        selected_collections.append(active_col)

    for col in selected_collections:
        yield from iter_meshes_in_collection(col, processed_objects)


def get_unselected_meshes(context):
    """Yield all mesh objects that are NOT part of the 'selected' set above."""
    selected_set = set(get_selected_meshes_and_collections(context))
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
# Operators — SELECTED
# -----------------------------

class MESH_OT_display_bounds_selected(bpy.types.Operator):
    bl_idname = "mesh.display_bounds_selected"
    bl_label = "Selected Bounds"
    bl_description = "Set the display type of selected meshes (incl. in selected collections/instances) to Bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(get_selected_meshes_and_collections(context), 'BOUNDS')
        return {'FINISHED'}


class MESH_OT_display_wire_selected(bpy.types.Operator):
    bl_idname = "mesh.display_wire_selected"
    bl_label = "Selected Wire"
    bl_description = "Set the display type of selected meshes (incl. in selected collections/instances) to Wire"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(get_selected_meshes_and_collections(context), 'WIRE')
        return {'FINISHED'}


class MESH_OT_display_solid_selected(bpy.types.Operator):
    bl_idname = "mesh.display_solid_selected"
    bl_label = "Selected Solid"
    bl_description = "Set the display type of selected meshes (incl. in selected collections/instances) to Solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(get_selected_meshes_and_collections(context), 'SOLID')
        return {'FINISHED'}


class MESH_OT_display_texture_selected(bpy.types.Operator):
    bl_idname = "mesh.display_texture_selected"
    bl_label = "Selected Textured"
    bl_description = "Set the display type of selected meshes (incl. in selected collections/instances) to Textured"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(get_selected_meshes_and_collections(context), 'TEXTURED')
        return {'FINISHED'}


# -----------------------------
# Operators — UNSELECTED (NEW)
# -----------------------------

class MESH_OT_display_bounds_unselected(bpy.types.Operator):
    bl_idname = "mesh.display_bounds_unselected"
    bl_label = "Unselected Bounds"
    bl_description = "Set the display type of unselected meshes to Bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(get_unselected_meshes(context), 'BOUNDS')
        return {'FINISHED'}


class MESH_OT_display_wire_unselected(bpy.types.Operator):
    bl_idname = "mesh.display_wire_unselected"
    bl_label = "Unselected Wire"
    bl_description = "Set the display type of unselected meshes to Wire"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(get_unselected_meshes(context), 'WIRE')
        return {'FINISHED'}


class MESH_OT_display_solid_unselected(bpy.types.Operator):
    bl_idname = "mesh.display_solid_unselected"
    bl_label = "Unselected Solid"
    bl_description = "Set the display type of unselected meshes to Solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(get_unselected_meshes(context), 'SOLID')
        return {'FINISHED'}


class MESH_OT_display_texture_unselected(bpy.types.Operator):
    bl_idname = "mesh.display_texture_unselected"
    bl_label = "Unselected Textured"
    bl_description = "Set the display type of unselected meshes to Textured"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _set_display_type(get_unselected_meshes(context), 'TEXTURED')
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

        # --- Unselected (NEW) ---
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

    # Unselected (NEW)
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
