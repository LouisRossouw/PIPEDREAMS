"""
Randomly animates objects dissearing in a randomised way, good for pixle art fade out
"""
import os
import random
import maya.cmds as cmds



def build_ui():
	""" Runs the UI """


	def execute(*args):
		""" executes the button """
		
		frame_START = cmds.intField(start_field, query=True, value=True)
		frame_END = cmds.intField(end_field, query=True, value=True)
			
		sel = cmds.ls(selection=True)
		selection_children = cmds.listRelatives(sel, ad=True)
		
		obj_list = []
		frame_range = []
		
		for obj in selection_children:
			if "Shape" not in obj:
				obj_list.append(obj)
				
				
		for frame in range(frame_START, frame_END + 1):
			frame_range.append(frame)
				
		random.shuffle(frame_range)
		random.shuffle(obj_list)
		
		# Key
		for obj in obj_list:
			
			frame = random.choice(frame_range)
			
			cmds.setKeyframe(obj + ".visibility" ,time=frame, v=1)
			cmds.setKeyframe(obj + ".visibility" ,time=frame + 1, v=0)
		
			
		
## UI
	project_name = os.getenv('PROJECT_NAME')
	window_title = 'RandomHide || ' + str(project_name)

	cmds.window(title=window_title, widthHeight=(400, 100), menuBar=True)

	cmds.columnLayout(adjustableColumn=True)
	cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), columnWidth=[(10, 100), (2, 250)])

	start_frame = cmds.playbackOptions(q=True, min=True)
	end_frame = cmds.playbackOptions(q=True, max=True)

	cmds.text(label='start_frame')
	start_field = cmds.intField('start_int', v=start_frame)

	cmds.text(label='end_frame')
	end_field = cmds.intField('end_int', v=end_frame)

	cmds.setParent( '..' )
	cmds.columnLayout(adjustableColumn=True)

	cmds.button(label='RandomHide',bgc=(0.65, 1, 0), command=execute)
	cmds.setParent('..', menu=True)

	cmds.showWindow()



if __name__ == "__main__":
	build_ui()
