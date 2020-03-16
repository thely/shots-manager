things to respond to:
- objects in the system are deleted
- actions are deleted
- objects or actions change names
- actions are added to objects in the system
- actions are added to objects not in the system

things it should do:
- actions can be added to/removed from shots
- actions


1. unassign an object (yes)
2. assign action to object

db interface: permastorage and filtering

An action can bbe associated with multiple objs. (normal)
An obj can be associated with more than one action. (not normal)

checking changes:
    - did our number of actions change?
        - if so, find parent
    - did any of their users change?
        - if so, loop through searchables to find the user(s)
        

Shot1 : CubeAction : Cube
Shot1 : CubeAction : Light

Shot2 : (CubeAction.001 : Cube)
Shot2 : CubeAssociation2
Shot2 : CubeAssociation3

Shot3 : CubeAssociation2

objects:
    - names?
    - current action (ref to table)
    - data type

actions:
    - names?
    - user count
    - has fake user

obj_action_links:
    - object (ref to table)
    - action (ref to table)
    - active/inactive?

shot:
    - type (folder or shot)
    - is active?
    - name
    - parent_id (-1 for base)

shots_links:
    - shot (ref to table)
    - obj_action (ref to table)


If no shot is currently selected when action is created, it goes in the base folder.




On assigned actions:
On unassigned actions:
        - adds user to the action
        
sql altering methods:
    - mute on object. unassigns live, but doesn't remove relationship, just inactivates. changes moves

    


