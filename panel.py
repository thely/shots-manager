class ShotFolderPanel(bpy.types.Panel):
	"""Organize actions into shots"""
	bl_label = "Shot Folders"
	bl_idname = "SHOTS_PT_organizerpanel"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "scene"

	def __init__(self):
		self.index = 0

	def draw(self, context):
		layout = self.layout
		obj = context.object

		row = layout.row()
		row.label(text="Actions!", icon='CAMERA_DATA')
		row = layout.row()
		row.operator("shots.dbinit") 
		
		row = layout.row()
		row.label(text="Assigned actions")
		moves = buddy.get_moves()
		box = layout.box()
		for m in moves:
			self.action_row(box, m[2], m[1], m[3], m[0])

		moves_free = buddy.get_free_moves()
		
		row = layout.row()
		row.label(text="Unassigned actions")
		box = layout.box()
		for m in moves_free:
			self.action_row(box, m[1])

	# Draw a single row for each action    
	def action_row(self, layout, action, object=None, state=None, move_id=None):
		row = layout.row()
		
		icon_obj = self.get_data_icon(object)
		obj_text = ""
		
		if object is not None:
			obj_text = object + " :: "
			row.context_pointer_set("object_mine", bpy.data.objects[object])
		
		icon_state = "HIDE_OFF" if state is not None and state is not 0 else "HIDE_ON"
		row.context_pointer_set("action_mine", bpy.data.actions[action])

		row.label(icon=icon_obj, text="")
		row.label(text=obj_text + action)
		row.label(icon=icon_state, text="")
		row.menu("SHOTS_MT_alter_action", text="", icon="DOWNARROW_HLT")



	# Search the objects collection to see who owns an action
	def find_action_parent(self, action):
		users = bpy.data.actions[action].users
		if users == 0:
			return ""
		count = 0
#        searchables = [bpy.data.objects, bpy.data.lights, bpy.data.cameras]
		
		for x in bpy.data.objects:
			print(x)
			if x.animation_data and x.animation_data.action:
				print(x.animation_data.action.name)
				print(action)
				if x.animation_data.action.name == action:
					return x.type
		
		return ""
	
	def get_data_icon(self, object=None):
		if object == None:
			return "ACTION"
		else:
			return bpy.data.objects[object].type + "_DATA"