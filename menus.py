class ShotsActionChange(bpy.types.Menu):
    bl_idname = "SHOTS_MT_alter_action"
    bl_label = "Alter action"
    
    def draw(self, context):
        pprint(context.space_data)
        layout = self.layout
        
        act = context.action_mine
        obj = context.object_mine
#        move = context.move_mine

        layout.operator("shots.unassign_action", text="Unassign " + act.name + " from " + obj.name).object_name = obj.name
        layout.operator("shots.assign_action").action_name = act.name
        
        op = layout.operator("shots.change_visible")
        op.action_name = act.name
        op.object_name = obj.name