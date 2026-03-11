import bpy



#===================================
    # --- Settings Panel ---
#===================================
class OBJECTDISPLAY_PT_objectdisplay_panel(bpy.types.Panel):
    bl_label = "Display Modes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "View"


    def draw(self, context):
        layout = self.layout
        select_method = ['Collection', 'All', 'Selected', 'Unselected']
        
        viewportBox = layout.box()
        viewportBox.label(text = "Viewport Visibility: " , icon = 'RESTRICT_VIEW_OFF')

        for selection in select_method:
            # --- Collection ---
            rowSelection = viewportBox.row(align = True)
            rowSelection.label(text = selection + ":")

            boundsOperator = rowSelection.operator("objectsdisplay.objects_viewport_display", text="", icon="PIVOT_BOUNDBOX")
            boundsOperator.select_method = selection.upper()
            boundsOperator.display_mode = 'BOUNDS'

            wireOperator = rowSelection.operator("objectsdisplay.objects_viewport_display", text="", icon="MOD_WIREFRAME")
            wireOperator.select_method = selection.upper()
            wireOperator.display_mode = 'WIRE'

            solidOperator = rowSelection.operator("objectsdisplay.objects_viewport_display", text="", icon="SHADING_SOLID")
            solidOperator.select_method = selection.upper()
            solidOperator.display_mode = 'SOLID'

            texturedOperator = rowSelection.operator("objectsdisplay.objects_viewport_display", text="", icon="TEXTURE")
            texturedOperator.select_method = selection.upper()
            texturedOperator.display_mode = 'TEXTURED'
