import psutil
import os











applications_list = ["maya.exe"]


search_taskManager = os.popen('wmic process get description, processid').read()


for app in applications_list:

    foundPID = search_taskManager.find(app)

    print(app, " - ", foundPID)


    # HIGH_PRIORITY_CLASS

    utilProcess = psutil.Process(foundPID)
    utilProcess.set_nice(psutil.LOW_PRIORITY_CLASS)
        

