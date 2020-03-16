class ShotsDBInit(bpy.types.Operator):
	bl_idname = "shots.dbinit"
	bl_label = "Initialize Actions DB"
	
	def __init__(self):
		self.has_run = False
	
	def execute(self, context):
		buddy.db_load()
		self.has_run = True
		
		return {'FINISHED'}

class ShotsUnassignAction(bpy.types.Operator):
	bl_idname = "shots.unassign_action"
	bl_label = "Unassign an action from an object"
	
	object_name: bpy.props.StringProperty(name="obj_name")
	
	def execute(self, context):
		buddy.unassign_object_action(self.object_name)
		obj = bpy.data.objects[self.object_name]
		obj.animation_data_clear()
		
		return {'FINISHED'}

class ShotsAssignAction(bpy.types.Operator):
	bl_idname = "shots.assign_action"
	bl_label = "Assign an action to an object"
	
	action_name: bpy.props.StringProperty(name="act_name")
	new_mom: bpy.props.StringProperty()
	
	@classmethod
	def poll(cls, context):
		return True
	
	def draw(self, context):
		row = self.layout
		row.label(text="Assign action to...?")
		
		row = self.layout
		row.prop_search(self, "new_mom", bpy.data, "objects")
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)
	
	def execute(self, context):
		buddy.set_move(self.new_mom, self.action_name)
		
		bpy.data.objects[self.new_mom].animation_data.action = bpy.data.actions[self.action_name]
		print(self.new_mom + " " + self.action_name)
		return {'FINISHED'}


class ShotsToggleVisible(bpy.types.Operator):
	bl_idname = "shots.toggle_visible"
	bl_label = "Change action visibility"
	
	action_name: bpy.props.StringProperty()
	object_name: bpy.props.StringProperty()
	
	def execute(self, context):
		state = buddy.toggle_visible(self.action_name, self.object_name)
		print(state)
#        print (self.action_name + " " + self.object_name)
		
		
		return {'FINISHED'}
