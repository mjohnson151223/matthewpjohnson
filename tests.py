import subprocess
import re
import sys

def readFile(path):
    file = open(path, 'r')
    data = file.read()
    file.close()
    re.sub('//.*?\n|/\*.*?\*/', '', data, flags=re.S)
    dataList = re.split('\n', data)
    dataList = [x.strip().replace(" ", "") for x in dataList if x != "\n" and x != '']
    dataList = [x for x in dataList if x[:2] != "//"]
    blockFound = False
    for i, item in enumerate(dataList):
        if "/*" in item:
            blockFound = True
            indexOfStartBlock = i
        if "*/" in item:
            indexOfEndBlock = i
    if blockFound:
        newList = []
        for i in range(len(dataList)):
            if i < indexOfStartBlock or i > indexOfEndBlock:
                newList.append(dataList[i])
        dataList = newList

    for i, x in enumerate(dataList):
        indexOfComment = x.find("//")
        if indexOfComment != -1:
            dataList[i] = x[:indexOfComment]
    return dataList

# Track failures
failed = False

def checkmyfunctionsHeader():
    global failed
    data = readFile("myfunctions.h")
    iostreamFound = False
    stdnamespaceFound = False
    prototypesHere = False

    data = [x.strip() for x in data if x != "\n"]

    for line in data:
        if "#include<iostream>" in line:
            iostreamFound = True
        if "usingnamespacestd;" in line:
            stdnamespaceFound = True
        if "voidpromptUser()" in line:
            prototypesHere = True

    if not iostreamFound or not stdnamespaceFound or not prototypesHere:
        print("Test 1: Failed; myfunctions.h incomplete")
        failed = True
    else:
        print("Test 1: Passed")

def checkmyfunctionsimplementation():
    global failed
    data = readFile("myfunctions.cpp")
    data = [x.strip() for x in data if x != "\n"]
    includeFound = False
    cinFound = False
    coutFound = False
    for line in data:
        if "#include\"myfunctions.h\"" in line:
            includeFound = True
        if "cin>>" in line.replace(" ", ""):
            cinFound = True
        if "cout<<" in line.replace(" ", ""):
            coutFound = True
    if not includeFound or not cinFound or not coutFound:
        print("Test 2: Failed; myfunctions.cpp incomplete")
        failed = True
    else:
        print("Test 2: Passed")

def checkmain():
    global failed
    coutCount = 0
    data = readFile("main.cpp")
    data = [x.strip() for x in data if x != "\n"]
    for line in data:
        if "cout<<" in line.replace(" ", ""):
            coutCount += 1
    if coutCount != 2:
        print("Test 3: Failed; main.cpp incomplete")
        failed = True
    else:
        print("Test 3: Passed")

def checkMakeAndRun():
    global failed
    try:
        makeResult = subprocess.call(['make'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Input to send to your program
        sample_input = "5\n10\n15\n"
        # Run program and send input
        proc = subprocess.Popen(
            "./averager",
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=sample_input)

        cleanResult = subprocess.call(['make', 'clean'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if makeResult != 0 or cleanResult != 0 or proc.returncode != 0:
            print("Test 4: Failed; code does not compile and run correctly")
            failed = True
        else:
            print("Test 4: Passed")
            print("Sample output:\n", stdout.strip())

    except Exception as e:
        print(f"Test 4: Failed; exception during build/run: {e}")
        failed = True

# Run tests
checkmyfunctionsHeader()
checkmyfunctionsimplementation()
checkmain()
checkMakeAndRun()

# Exit appropriately for GitHub Actions
if failed:
    sys.exit(1)
else:
    sys.exit(0)