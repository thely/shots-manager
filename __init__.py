import bpy
from pprint import pprint
import sqlite3

bl_info = {
    "name": "MyAddon",
    "description": "A demo addon",
    "author": "myname",
    "version": (1, 0, 0),
    "blender": (2, 7, 9),
    "wiki_url": "my github url here",
    "tracker_url": "my github url here/issues",
    "category": "Animation"
}

classList = [ShotFolderPanel, ShotsDBInit, ShotsActionChange, ShotsUnassignAction, ShotsAssignAction, ShotsToggleVisible]

buddy = DBFriend()



def register():
	for c in classList:
		bpy.utils.register_class(c)
		
#    bpy.types.Scene.current_object = bpy.props.StringProperty(name="Object to alter")


def unregister():
	for c in classList:
		bpy.utils.unregister_class(c)


if __name__ == "__main__":
	register()