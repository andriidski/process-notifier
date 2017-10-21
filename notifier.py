# author: Andrii Dobroshynskyi
import os
import subprocess
import time

flag = "--NOTIFY"
currentlyRunningFlagged = {}

debug = False

# cleans up process name of --notify flag for display in notification
def cleanProcessName(processString):
    tokenized = processString.split()
    cleaned = ""
    for i in range(0, len(tokenized) - 1):
        cleaned += tokenized[i]
        cleaned += " "
    return cleaned.strip()

# send notification
def sendNotification(text):
    title = "Notifier"
    subtitle = "Terminal process completed"
    sound = "Pop.aiff"
    os.system("""
              osascript -e 'display notification "{}" with title "{}" subtitle "{}" sound name "{}"'
              """.format(text, title, subtitle, sound))

# process any processes that might have just finished running
def cleanUpFinishedProcesses(currentProcs):
    currentProcessNames = []
    for proc in currentProcs:
        currentProcessNames.append(proc[0])

    for (name,process) in currentlyRunningFlagged.items():
        if name not in currentProcessNames:
            # trigger notification
            if debug:
                print "process ", name, " got finished"
            sendNotification(cleanProcessName(name))
            currentlyRunningFlagged.pop(name, None)

# add any processes that just started running and have been flagged to be notified
def updateRunningList(procs):
    for processTuple in procs:
        if processTuple[0] not in currentlyRunningFlagged.keys():
            currentlyRunningFlagged[processTuple[0]] = processTuple[1]

# get processes running on system
def getProcesses():
    ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
    processes = ps.split('\n')
    nfields = len(processes[0].split()) - 1
    procList = []
    for row in processes[1:]:
        procList.append(row.split(None, nfields))
    return procList

# filter running system processes to find ones that are flagged
def getFlaggedProcesses(procs):
    flagged = []
    for index,processInfo in enumerate(procs):
        for term in processInfo:
            words = term.split()
            if flag in words:
                if debug:
                    print "FOUND RUNNING WITH FLAG"
                flagged.append((term,processInfo))
    return flagged

# interval running
starttime = time.time()
timeInterval = 2.0

print("monitoring processes with [" + flag + "] flag...")

while True:
    if debug:
        print "running"
    # fetch processes and process data
    procs = getProcesses()
    flagged = getFlaggedProcesses(procs)
    updateRunningList(flagged)
    cleanUpFinishedProcesses(flagged)
    if debug:
        print currentlyRunningFlagged
    time.sleep(timeInterval - ((time.time() - starttime) % timeInterval))
