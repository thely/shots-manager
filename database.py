class DBFriend:
	bl_idname = "shots.dbfriend"
#    file_loc: bpy.props.StringProperty()
	def __init__(self, path="//db.sqlite3"):
		self.path = bpy.path.abspath(path)
	
	def dbconn(self):
		con = sqlite3.connect(self.path)
		return con
	
	# Generate the tables if the file is just opening + no sqlite exists
	def tables_init(self, con, cur):
		actions_sql = """
		CREATE TABLE IF NOT EXISTS actions (
			action_id integer PRIMARY KEY,
			action_name text NOT NULL,
			users integer NOT NULL,
			has_fake boolean NOT NULL
		)"""
		cur.execute(actions_sql)
		
		objs_sql = """
		CREATE TABLE IF NOT EXISTS objects (
			object_id integer PRIMARY KEY,
			object_name text NOT NULL,
			current_action integer,
			FOREIGN KEY (current_action) REFERENCES actions (action_id)
		)"""
		cur.execute(objs_sql)
		
		moves_sql = """
		CREATE TABLE IF NOT EXISTS moves (
			move_id integer PRIMARY KEY,
			action_id integer,
			object_id integer,
			action_visible integer DEFAULT 1,
			FOREIGN KEY (action_id) REFERENCES actions (action_id),
			FOREIGN KEY (object_id) REFERENCES objects (object_id)
		)"""
		cur.execute(moves_sql)
		
		con.commit()
	
	# Populate the tables with action data, when we're first activated
	def populate_new_data(self, con, cur):
		
		# base state of actions
		template = "INSERT INTO actions (action_name, users, has_fake) VALUES (?,?,?)"
		for act in bpy.data.actions:
			cur.execute(template, (act.name, act.users, act.use_fake_user))
		
		print("---our actions:")
		pprint(self.get_table(cur, "actions"))
		
		# base state of objects
		template = "INSERT INTO objects (object_name, current_action) VALUES (?,?)"
		for obj in bpy.data.objects:
			if obj.animation_data and obj.animation_data.action:
				sel_temp = "SELECT action_id FROM actions WHERE action_name = ?"
				cur.execute(sel_temp, (obj.animation_data.action.name,))
				act_id = cur.fetchone()
				cur.execute(template, (obj.name, act_id[0]))
		
		print("---our objects:")
		pprint(self.get_table(cur, "objects"))
		
		# figuring out the base state of the moves
		cur.execute("SELECT object_id, current_action FROM objects")
		moves = cur.fetchall()
		template = "INSERT INTO moves (object_id, action_id) VALUES(?, ?)"
		for m in moves:
			cur.execute(template, m) 
		
		print("---our moves:")
		pprint(self.get_table(cur, "moves"))
		
		con.commit()
	
	def get_moves(self):
#        print("---getting moves?")
		con = self.dbconn()
		cur = con.cursor()
		query = """
			SELECT moves.move_id, objects.object_name, actions.action_name, moves.action_visible
			FROM moves
			INNER JOIN actions on actions.action_id == moves.action_id
			INNER JOIN objects on objects.object_id == moves.object_id
		"""
		
		cur.execute(query)
		result = cur.fetchall()
		cur.close()
#        print(result)
		
		return result
	
	def get_free_moves(self):
		con = self.dbconn()
		cur = con.cursor()
		query = """
			SELECT action_id
			FROM actions
			EXCEPT
			SELECT action_id
			FROM moves
		"""
		
		cur.execute(query)
		list = cur.fetchall()
		result = [k[0] for k in list]
		
		query = "SELECT action_id, action_name FROM actions WHERE action_id IN (%s)" % ",".join("?" * len(result))
		cur.execute(query, result)
		result = cur.fetchall()
		cur.close()
		
		return result
	
	# Testing: delete the whole DB and start afresh
	def temporary_clear(self, con, cur):
		tables = ["objects", "actions", "moves"]
		
		for t in tables:
#            cur.execute("DELETE FROM IF EXISTS " + t)
			cur.execute("DROP TABLE IF EXISTS " + t)

	# Full init parent  
	def db_load(self):
		con = self.dbconn()
		cur = con.cursor()
		
		self.temporary_clear(con, cur)
		self.tables_init(con, cur)
		self.populate_new_data(con, cur)
	
	def get_table(self, cur, table):
		query = "SELECT * FROM %s" % (table)
		cur.execute(query)
		result = cur.fetchall()
		return result
	
	def check_state(self, arr):
		con = self.dbconn()
		cur = con.cursor()
	
	# remove a move from the set
	def unassign_object_action(self, obj_name):
		print("---removing a move---")
		con = self.dbconn()
		cur = con.cursor()
		
		obj_id = self.get_var_from_table(cur, "objects", "object_name", "object_id", obj_name)
		
		query = "DELETE FROM moves WHERE object_id = ?"
		cur.execute(query, (int(obj_id),))
		pprint(self.get_table(cur, "moves"))
		
		con.commit()
		cur.close()
	
	
	def toggle_move_active(self, cur, move, state):
		query = "UPDATE moves SET action_visible = ? WHERE move_id = ?"
		cur.execute(query, (state, move))
	
	# handle visibility when an object has more than one action
	def change_active_action(self, solo, obj_id):
		con = self.dbconn()
		cur = con.cursor()
		
		query = "SELECT move_id FROM moves WHERE object_id = ?"
		cur.execute(query, (int(obj_id),))
		
		ids = cur.fetchall()
		print(ids)
		
		for i in ids:
			state = 1 if i[0] == solo else 0
			print(str(i[0]) + " " + str(state))
			self.toggle_move_active(cur, i[0], state)
		
		cur.close()
		con.commit()
		
	# newly assign an action to an object
	def create_move(self, object_name, action_name):
		con = self.dbconn()
		cur = con.cursor()
		
		# check if this object - action relationship exists already
		act_id = self.get_var_from_table(cur, "actions", "action_name", "action_id", action_name)
		obj_id = self.get_var_from_table(cur, "objects", "object_name", "object_id", object_name)
		
		query = "SELECT COUNT(*) FROM moves WHERE action_id = ? AND object_id = ?"
		cur.execute(query, (act_id, obj_id))
		count = cur.fetchone()[0]
		
		# add to db if it's brand new
		retval = -1
		if count == 0:
			query = "INSERT INTO moves (action_id, object_id) VALUES (?,?)"
			cur.execute(query, (act_id, obj_id))
			retval = (cur.lastrowid, obj_id)
		else:
			print("it's a dupe!")
		
		cur.close()
		con.commit()
		return retval 
	
	def set_move_visible(self, object_name, action_name):
		con = self.dbconn()
		cur = con.cursor()
		
#        act_id = self.get_var_from_table(cur, "actions", "action_name", "action_id", action_name)
#        obj_id = self.get_var_from_table(cur, "objects", "object_name", "object_id", object_name)
#        
	
	def set_move(self, object_name, action_name):
		state = self.create_move(object_name, action_name)
		
		if isinstance(state, int):
			return
		else:
			self.change_active_action(state[0], state[1])
	
	def get_var_from_table(self, cur, table, column_have, column_need, val):
		query = "SELECT (%s) FROM %s WHERE %s = (?)" % (column_need, table, column_have)

		print(val)
		print(query)
		cur.execute(query, (val,))
		result = cur.fetchone()[0]
		pprint(result)
		
		return result