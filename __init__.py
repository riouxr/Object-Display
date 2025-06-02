import bpy

class VIEW3D_PT_display(bpy.types.Panel):
    bl_label = "Display Modes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "View"

    def draw(self, context):
        layout = self.layout
        
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

def get_selected_meshes_and_collections(context):
    """
    Generator that yields mesh objects that are either directly selected,
    within selected collection instances (empties instancing collections),
    or within selected collections (including nested collections).
    """
    # Set to keep track of processed objects to avoid duplicates
    processed_objects = set()

    # Process directly selected mesh objects
    for obj in context.selected_objects:
        if obj.type == 'MESH' and obj not in processed_objects:
            processed_objects.add(obj)
            yield obj
        elif obj.type == 'EMPTY' and obj.instance_type == 'COLLECTION' and obj.instance_collection:
            # Handle mesh objects in collection instances referenced by selected empties
            for inst_obj in obj.instance_collection.objects:
                if inst_obj.type == 'MESH' and inst_obj not in processed_objects:
                    processed_objects.add(inst_obj)
                    yield inst_obj

    # Process mesh objects in selected collections
    def get_meshes_from_collection(collection, processed):
        """Recursively yield mesh objects from a collection and its subcollections."""
        for obj in collection.objects:
            if obj.type == 'MESH' and obj not in processed:
                processed.add(obj)
                yield obj
        for subcollection in collection.children:
            yield from get_meshes_from_collection(subcollection, processed)

    # Check selected collections in the outliner or viewport
    selected_collections = []
    # Try to get collections from selected_ids (outliner selections)
    if hasattr(context, 'selected_ids') and context.selected_ids:
        for item in context.selected_ids:
            if item.bl_rna.identifier == 'Collection':
                selected_collections.append(item)

    # Also check the active layer collection (viewport context)
    active_collection = context.view_layer.active_layer_collection.collection
    if active_collection and active_collection not in selected_collections:
        selected_collections.append(active_collection)

    # Process all selected collections
    for collection in selected_collections:
        yield from get_meshes_from_collection(collection, processed_objects)

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

class MESH_OT_display_bounds_selected(bpy.types.Operator):
    bl_idname = "mesh.display_bounds_selected"
    bl_label = "Selected Bounds"
    bl_description = "Set the display type of selected meshes and collection instances to bounds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = 0
        for obj in get_selected_meshes_and_collections(context):
            obj.display_type = 'BOUNDS'
            count += 1
        print(f"Set {count} objects to BOUNDS display")
        return {'FINISHED'}

class MESH_OT_display_texture_selected(bpy.types.Operator):
    bl_idname = "mesh.display_texture_selected"
    bl_label = "Selected Textured"
    bl_description = "Set the display type of selected meshes and collection instances to texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = 0
        for obj in get_selected_meshes_and_collections(context):
            obj.display_type = 'TEXTURED'
            count += 1
        print(f"Set {count} objects to TEXTURED display")
        return {'FINISHED'}

class MESH_OT_display_wire_selected(bpy.types.Operator):
    bl_idname = "mesh.display_wire_selected"
    bl_label = "Selected Wire"
    bl_description = "Set the display type of selected meshes and collection instances to wire"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        count = 0
        for obj in get_selected_meshes_and_collections(context):
            obj.display_type = 'WIRE'
            count += 1
        print(f"Set {count} objects to WIRE display")
        return {'FINISHED'}

class MESH_OT_display_solid_selected(bpy.types.Operator):
    bl_idname = "mesh.display_solid_selected"
    bl_label = "Selected Solid"
    bl_description = "Set the display type of selected meshes and collection instances to solid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        count = 0
        for obj in get_selected_meshes_and_collections(context):
            obj.display_type = 'SOLID'
            count += 1
        print(f"Set {count} objects to SOLID display")
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