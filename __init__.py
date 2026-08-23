bl_info = {
    "name": "Display Modes — Selected / Unselected / All",
    "author": "ChatGPT + User",
    "version": (1, 4, 0),
    "blender": (3, 0, 0),
    "location": "3D Viewport > Sidebar > View",
    "description": "Icon-only controls to set object display modes for Selected, Unselected, or All mesh objects",
    "category": "3D View",
}


import bpy

from . import operators, ui


#===================================
    # --- Object Menu ---
#===================================
class OBJECTDISPLAY_MT_viewport_object_submenu(bpy.types.Menu):
    bl_label = "Object Display Mode"
    bl_idname = "OBJECTDISPLAY_MT_viewport_object_submenu"

    def draw(self, context):
        layout = self.layout

        op_bounds = layout.operator(
            'objectsdisplay.objects_viewport_display',
            text="Display selected as bounds",
            icon='PIVOT_BOUNDBOX'
        )
        op_bounds.select_method = 'SELECTED'
        op_bounds.display_mode = 'BOUNDS'

        op_wire = layout.operator(
            'objectsdisplay.objects_viewport_display',
            text="Display selected as wire",
            icon='MOD_WIREFRAME'
        )
        op_wire.select_method = 'SELECTED'
        op_wire.display_mode = 'WIRE'

        op_solid = layout.operator(
            'objectsdisplay.objects_viewport_display',
            text="Display selected as solid",
            icon='SHADING_SOLID'
        )
        op_solid.select_method = 'SELECTED'
        op_solid.display_mode = 'SOLID'

        op_textured = layout.operator(
            'objectsdisplay.objects_viewport_display',
            text="Display selected as textured",
            icon='TEXTURE'
        )
        op_textured.select_method = 'SELECTED'
        op_textured.display_mode = 'TEXTURED'


class OBJECTDISPLAY_MT_outliner_object_submenu(bpy.types.Menu):
    bl_label = "Object Display Mode"
    bl_idname = "OBJECTDISPLAY_MT_outliner_object_submenu"

    def draw(self, context):
        layout = self.layout
        
        op_bounds = layout.operator('objectsdisplay.objects_viewport_display', text="Display selected as bounds", icon='PIVOT_BOUNDBOX')
        op_bounds.select_method = 'SELECTED'
        op_bounds.display_mode = 'BOUNDS'
        
        op_wire = layout.operator('objectsdisplay.objects_viewport_display', text="Display selected as wire", icon='MOD_WIREFRAME')
        op_wire.select_method = 'SELECTED'
        op_wire.display_mode = 'WIRE'
        
        op_solid = layout.operator('objectsdisplay.objects_viewport_display', text="Display selected as solid", icon='SHADING_SOLID')
        op_solid.select_method = 'SELECTED'
        op_solid.display_mode = 'SOLID'
        
        op_textured = layout.operator('objectsdisplay.objects_viewport_display', text="Display selected as textured", icon='TEXTURE')
        op_textured.select_method = 'SELECTED'
        op_textured.display_mode = 'TEXTURED'


#===================================
    # --- Collection Menu ---
#===================================
class OBJECTDISPLAY_MT_outliner_collection_submenu(bpy.types.Menu):
    bl_label = "Object Display Mode"
    bl_idname = "OBJECTDISPLAY_MT_outliner_collection_submenu"

    def draw(self, context):
        layout = self.layout
        
        # Add operators with different display modes for selected objects
        op_bounds = layout.operator('objectsdisplay.objects_viewport_display', text="Display collection as bounds", icon='PIVOT_BOUNDBOX')
        op_bounds.select_method = 'COLLECTION'
        op_bounds.display_mode = 'BOUNDS'
        
        op_wire = layout.operator('objectsdisplay.objects_viewport_display', text="Display collection as wire", icon='MOD_WIREFRAME')
        op_wire.select_method = 'COLLECTION'
        op_wire.display_mode = 'WIRE'
        
        op_solid = layout.operator('objectsdisplay.objects_viewport_display', text="Display collection as solid", icon='SHADING_SOLID')
        op_solid.select_method = 'COLLECTION'
        op_solid.display_mode = 'SOLID'
        
        op_textured = layout.operator('objectsdisplay.objects_viewport_display', text="Display collection as textured", icon='TEXTURE')
        op_textured.select_method = 'COLLECTION'
        op_textured.display_mode = 'TEXTURED'


#===================================
    # --- Registration ---
#===================================
classes = (
    # ui
    ui.OBJECTDISPLAY_PT_objectdisplay_panel,

    # operators
    operators.OBJECTSDISPLAY_OT_objects_viewport_display,
    
    # menus
    OBJECTDISPLAY_MT_viewport_object_submenu,
    OBJECTDISPLAY_MT_outliner_object_submenu,
    OBJECTDISPLAY_MT_outliner_collection_submenu,
)

def menu_func(self, context):
    layout = self.layout
    layout.separator()
    
    layout.menu("OBJECTDISPLAY_MT_outliner_object_submenu")

def menu_func_viewport(self, context):
    # Only show the menu in Object Mode.
    if context.mode != 'OBJECT':
        return

    layout = self.layout
    layout.separator()
    layout.menu("OBJECTDISPLAY_MT_viewport_object_submenu")


def menu_func_collection(self, context):
    layout = self.layout
    layout.separator()
    
    layout.menu("OBJECTDISPLAY_MT_outliner_collection_submenu")


def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.OUTLINER_MT_context_menu.append(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func_viewport)
    bpy.types.OUTLINER_MT_object.append(menu_func)
    bpy.types.OUTLINER_MT_collection.append(menu_func_collection)



def unregister():
    try:
        bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func_viewport)
    except (AttributeError, ValueError):
        pass
    try:
        bpy.types.OUTLINER_MT_context_menu.remove(menu_func)
    except (AttributeError, ValueError):
        pass
    try:
        bpy.types.OUTLINER_MT_object.remove(menu_func)
    except (AttributeError, ValueError):
        pass
    try:
        bpy.types.OUTLINER_MT_collection.remove(menu_func_collection)
    except (AttributeError, ValueError):
        pass

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
