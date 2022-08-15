
# -----------------------------------
# Studio Library
# www.studiolibrary.com
# -----------------------------------

import os
import sys

def launchStudioLib():
    
	if not os.path.exists(r'C:\Users\user-pc\Desktop\dump\studiolibrary-2.9.6.b3\src'):
		raise IOError(r'The source path "C:\Users\user-pc\Desktop\dump\studiolibrary-2.9.6.b3\src" does not exist!')
		
	if r'C:\Users\user-pc\Desktop\dump\studiolibrary-2.9.6.b3\src' not in sys.path:
		sys.path.insert(0, r'C:\Users\user-pc\Desktop\dump\studiolibrary-2.9.6.b3\src')
		
	import studiolibrary
	studiolibrary.main()




