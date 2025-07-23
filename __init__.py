import bpy

# -----------------------------
# Collection Picker + Panel UI
# -----------------------------

class VIEW3D_PT_display(bpy.types.Panel):
    bl_label = "Display Modes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "View"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        layout.separator()

        row = layout.row()
        row.operator("mesh.display_texture_selected", text="Textured Selected", icon="TEXTURE")
        row = layout.row()
        row.operator("mesh.display_solid_selected", text="Solid Selected", icon="SHADING_SOLID")
        row = layout.row()
        row.operator("mesh.display_wire_selected", text="Wire Selected", icon="MOD_WIREFRAME")
        row = layout.row()
        row.operator("mesh.display_bounds_selected", text="Bounds Selected", icon="PIVOT_BOUNDBOX")        

        layout.separator()

        row = layout.row()
        row.operator("mesh.display_texture_all", text="All Textured", icon="TEXTURE")
        row = layout.row()
        row.operator("mesh.display_solid_all", text="All Solid", icon="SHADING_SOLID")
        row = layout.row()
        row.operator("mesh.display_wire_all", text="All Wire", icon="MOD_WIREFRAME")
        row = layout.row()
        row.operator("mesh.display_bounds_all", text="All Bounds", icon="PIVOT_BOUNDBOX")

# -----------------------------
# Utility: Get selected or dropdown collection meshes
# -----------------------------
def get_outliner_selected_collections():
    """Get collections explicitly selected (blue highlight) in the Outliner"""
    selected_collections = []
    
    # Check all windows and their screen for Outliner areas
    for window in bpy.context.window_manager.windows:
        screen = window.screen  # Use singular 'screen' instead of 'screens'
        for area in screen.areas:
            if area.type == 'OUTLINER':
                with bpy.context.temp_override(window=window, screen=screen, area=area):
                    outliner_context = bpy.context
                    if hasattr(outliner_context, 'selected_ids'):
                        for item in outliner_context.selected_ids:
                            if isinstance(item, bpy.types.Collection):
                                selected_collections.append(item)
                                print(f"[OUTLINER] Found selected collection: {item.name}")
    
    if not selected_collections:
        print("[OUTLINER] No collections in selected_ids")
    
    return selected_collections

def get_selected_meshes_and_collections(context):
    """
    Returns a list of unique mesh objects:
    - From selected objects in the 3D viewport
    - From collections explicitly selected in the Outliner (blue highlight)
    - From active collection if no viewport objects are selected
    """
    processed = set()
    result = []

    # 1. Add selected mesh objects from the 3D viewport
    print(f"\n=== VIEWPORT SELECTED OBJECTS ===")
    for obj in context.selected_objects:
        if obj.type == 'MESH' and obj.name not in processed:
            result.append(obj)
            processed.add(obj.name)
            print(f"[VIEWPORT] Added {obj.name}")

    # 2. Add mesh objects from collections explicitly selected in the Outliner
    print(f"\n=== OUTLINER SELECTED COLLECTIONS ===")
    selected_collections = get_outliner_selected_collections()
    
    if selected_collections:
        for collection in selected_collections:
            print(f"[COLLECTION] Processing {collection.name}")
            for obj in collection.objects:
                if obj.type == 'MESH' and obj.name not in processed:
                    result.append(obj)
                    processed.add(obj.name)
                    print(f"  - Added {obj.name} from collection")
    else:
        # Fallback to active collection only if no viewport objects are selected
        if not context.selected_objects:
            active_collection = bpy.context.view_layer.active_layer_collection
            if active_collection and active_collection.collection:
                collection = active_collection.collection
                print(f"[OUTLINER] No selected collections, using active collection: {collection.name}")
                print(f"[COLLECTION] Processing {collection.name}")
                for obj in collection.objects:
                    if obj.type == 'MESH' and obj.name not in processed:
                        result.append(obj)
                        processed.add(obj.name)
                        print(f"  - Added {obj.name} from collection")
        else:
            print("No collections selected in Outliner")

    print(f"Total objects to process: {len(result)}")
    return result
# -----------------------------
# Operators
# -----------------------------

# === ALL OBJECTS OPERATORS ===

class MESH_OT_display_bounds_all(bpy.types.Operator):
    bl_idname = "mesh.display_bounds_all"
    bl_label = "All Bounds"
    bl_description = "Set the display type of all meshes in the scene to bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                obj.display_type = 'BOUNDS'
        return {'FINISHED'}

class MESH_OT_display_texture_all(bpy.types.Operator):
    bl_idname = "mesh.display_texture_all"
    bl_label = "All Textured"
    bl_description = "Set the display type of all meshes in the scene to texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                obj.display_type = 'TEXTURED'
        return {'FINISHED'}

class MESH_OT_display_wire_all(bpy.types.Operator):
    bl_idname = "mesh.display_wire_all"
    bl_label = "All Wire"
    bl_description = "Set the display type of all meshes in the scene to wire"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                obj.display_type = 'WIRE'
        return {'FINISHED'}

class MESH_OT_display_solid_all(bpy.types.Operator):
    bl_idname = "mesh.display_solid_all"
    bl_label = "All Solid"
    bl_description = "Set the display type of all meshes in the scene to solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.scene.objects:
            if obj.type == 'MESH':
                obj.display_type = 'SOLID'
        return {'FINISHED'}

# === SELECTED OBJECTS OPERATORS ===

class MESH_OT_display_bounds_selected(bpy.types.Operator):
    bl_idname = "mesh.display_bounds_selected"
    bl_label = "Selected Bounds"
    bl_description = "Set the display type of selected meshes and collection-picked meshes to bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = 0
        meshes = get_selected_meshes_and_collections(context)
        for obj in meshes:
            obj.display_type = 'BOUNDS'
            print(f"→ {obj.name} now set to BOUNDS")
            count += 1
        print(f"Set {count} objects to BOUNDS display")
        return {'FINISHED'}

class MESH_OT_display_texture_selected(bpy.types.Operator):
    bl_idname = "mesh.display_texture_selected"
    bl_label = "Selected Textured"
    bl_description = "Set the display type of selected meshes and collection-picked meshes to texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = 0
        meshes = get_selected_meshes_and_collections(context)
        for obj in meshes:
            obj.display_type = 'TEXTURED'
            print(f"→ {obj.name} now set to TEXTURED")
            count += 1
        print(f"Set {count} objects to TEXTURED display")
        return {'FINISHED'}

class MESH_OT_display_wire_selected(bpy.types.Operator):
    bl_idname = "mesh.display_wire_selected"
    bl_label = "Selected Wire"
    bl_description = "Set the display type of selected meshes and collection-picked meshes to wire"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        count = 0
        meshes = get_selected_meshes_and_collections(context)
        for obj in meshes:
            obj.display_type = 'WIRE'
            print(f"→ {obj.name} now set to WIRE")
            count += 1
        print(f"Set {count} objects to WIRE display")
        return {'FINISHED'}

class MESH_OT_display_solid_selected(bpy.types.Operator):
    bl_idname = "mesh.display_solid_selected"
    bl_label = "Selected Solid"
    bl_description = "Set the display type of selected meshes and collection-picked meshes to solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = 0
        meshes = get_selected_meshes_and_collections(context)
        for obj in meshes:
            print(f"→ {obj.name} (was: {obj.display_type}) → setting to SOLID")
            obj.display_type = 'SOLID'
            print(f"✓ {obj.name} now: {obj.display_type}")
            count += 1
        print(f"Set {count} objects to SOLID display")
        return {'FINISHED'}

# -----------------------------
# Registration
# -----------------------------

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