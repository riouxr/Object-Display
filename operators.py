import bpy



class OBJECTSDISPLAY_OT_objects_viewport_display(bpy.types.Operator):
    bl_idname = "objectsdisplay.objects_viewport_display"
    bl_label = "Objects Viewport Display"
    bl_description = "Select objects by certain criteria and set their viewport display mode"
    bl_options = {'REGISTER', 'UNDO'}

    
    select_method : bpy.props.EnumProperty(
        name = "Select Method",
        description = "Method to select objects",
        items = [
        ('ALL', "All", "All objects", 0),
        ('SELECTED', "Selected", "Selected objects", 1),
        ('UNSELECTED', "Unselected", "Unselected objects", 2),
        ('COLLECTION', "Collection", "Collection objects", 3),
        ],
        default = 'SELECTED'
    )

    display_mode : bpy.props.EnumProperty(
        name = "Display Mode",
        description = "Display mode to set to objects",
        items = [
        ('BOUNDS', "Bounds", "Bounds mode", 0),
        ('WIRE', "Wire", "Wire mode", 1),
        ('SOLID', "Solid", "Solid mode", 2),
        ('TEXTURED', "Textured", "Textured mode", 3),
        ],
        default = 'TEXTURED'
    )


    def iter_selected_meshes(self, context):
        """Yield ONLY mesh objects that are currently selected in the viewport."""
        if not context.selected_objects:
            self.report({'INFO'}, "No objects are selected")
            return []

        selected_set = context.selected_objects
        return selected_set


    def iter_unselected_meshes(self, context):
        """Yield ONLY mesh objects in the scene that are NOT selected."""
        if not context.selected_objects:
            self.report({'INFO'}, "No objects are selected. Operate on all objects instead")
            return []

        selected_set = context.selected_objects
        for obj in context.scene.objects:
            if obj not in selected_set:
                yield obj


    def iter_collection_meshes(self, context):
        """Yield ONLY mesh objects in the given collection."""
        active_layer_coll = context.view_layer.active_layer_collection

        if active_layer_coll == context.view_layer.layer_collection:
            self.report({'WARNING'}, "Select a specific collection, not the entire scene layer")
            return []

        collection = context.view_layer.active_layer_collection.collection
        if not collection.all_objects:
            self.report({'INFO'}, "No objects inside the collection")
            return []

        return collection.all_objects
    
    def set_collection_name(self, context, display_mode):
        collection = context.view_layer.active_layer_collection.collection

        # Skip the Scene Collection (master) and any linked/override collections — their name is read-only
        if collection == context.scene.collection or collection.library is not None or collection.override_library is not None:
            self.report({'INFO'}, "Active collection name is read-only; skipping rename")
            return

        strip_suffixes = (
            " WIRE", " BOUNDS", " SOLID", " TEXTURED",
            " Wire", " Bounds",  " Solid", " Textured",
            "-WIRE", "-BOUNDS", "-SOLID", "-TEXTURED",
            "-Wire", "-Bounds",  "-Solid", "-Textured",
            "_WIRE", "_BOUNDS", "_SOLID", "_TEXTURED",
            "_Wire", "_Bounds",  "_Solid", "_Textured",
        )
        for suffix in strip_suffixes:
            if collection.name.endswith(suffix):
                collection.name = collection.name[:-len(suffix)]
                break

        if display_mode in ('WIRE', 'BOUNDS'):
            collection.name += "_" + display_mode


    def set_display_type(self, contetx, objs, display_mode):
        for obj in objs:
            try:
                obj.display_type = display_mode
            except Exception:
                pass


    def execute(self, context):       
        objects = []

        match self.select_method:
            case 'ALL':
                objects = context.scene.objects

            case 'SELECTED':
                objects = self.iter_selected_meshes(context)

            case 'UNSELECTED':
                objects = self.iter_unselected_meshes(context)

            case 'COLLECTION':
                objects = self.iter_collection_meshes(context)
                self.set_collection_name(context, self.display_mode)

        self.set_display_type(context, objects, self.display_mode)

        return {'FINISHED'}
    
    @classmethod    
    def description(cls, context, properties):
        description = ""
        start_string = "Select " 
        mid_string = " objects and set their viewport display mode to "

        select_method = properties.select_method
        display_mode = properties.display_mode

        match select_method:
            case 'ALL':
                description = start_string + "all" + mid_string
            case 'SELECTED':
                description = start_string + "selected" + mid_string
            case 'UNSELECTED':
                description = start_string + "unselected" + mid_string
            case 'COLLECTION':
                description = start_string + "collection" + mid_string

        match display_mode:
            case 'BOUNDS':
                description += "Bounds"
            case 'WIRE':
                description += "Wire"
            case 'SOLID':
                description += "Solid"
            case 'TEXTURED':
                description += "Textured"

        return description
