import json
import logging.handlers
import logging.handlers
import optparse
import time

from Commands import *

parser = optparse.OptionParser("usage: %prog [options] arg1 arg2")
parser.add_option("-s", "--script path", dest="ScriptPath", default="input/script/path", type="string",
                  help="specify script path to run on")
parser.add_option("-o", "--output", dest="OutputLogFile", default="output/script/path", type="string",
                  help="output log file to run on")
(options, args) = parser.parse_args()
args = parser.parse_args()
if len(args) != 2:
    parser.error("INCORRECT NUM OF ARGS")
    ScriptPath = options.ScriptPath
    OutputLogFile = options.OutputLogFile


sc = args[0].ScriptPath
output = args[0].OutputLogFile
sc = "D:\Tenorshare\script.txt"
output = "D:\Tenorshare\Outputt"
# Reads The Input Script File 'sc'
def ReadScript():
    global filehandle
    dataofcommand = []
    JSONData = ParseJSON()

    ExecutedCommands = 0
    try:
        filehandle = open(sc, "r")
    except FileNotFoundError:
        print("Make Sure The Directory Path Is Correct")
        exit(1)
    # logging.basicConfig(filename="Output.log", level=logging.DEBUG,
    #                     format='%(asctime)s:%(levelname)s:%(message)s')
    #
    # with open('Output.log', 'w'):
    #     pass

    while True:
        # read a single line
        line = filehandle.readline()
        if not line:
            break
        f = line.split()  # f contains commands with its data

        CommandType = f[0].split(' ', 1)[0]

        if CommandType == 'Grep' or CommandType == 'Categorize' or CommandType == 'Mv_last':
            for i in range(len(f) - 1):
                c = f[i + 1].replace("<", '').replace(">", '')  # c contains command data splitted
                dataofcommand.append(c)
            if int(JSONData[' Max_commands ']) < ExecutedCommands + 1:
                print("You Exceeded The Max Number Of Executed Commands!")
                break
            Commands.getCommand(CommandType, dataofcommand, JSONData, ExecutedCommands)
            ExecutedCommands += 1
            dataofcommand.clear()
        else:
            print("Invalid Command Type")

    filehandle.close()


def ParseJSON():
    myjsonfile = open("configuration.json", 'r')
    data = myjsonfile.read()
    JSONData = json.loads(data)
    return JSONData


def Logging(ResultDict):
    JSONData = ParseJSON()
    count = 0
    for value in range(len(Commands.Passed)):
        if Commands.Passed[value] == 1:
            count += 1
    if count == len(Commands.Passed):
        passed = "PASSED"
    else:
        passed = "FAILED"

    LOG_FILENAME = f'Output{passed}.log'
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)

    # Check if log exists and should therefore be rolled
    needRoll = os.path.isfile(LOG_FILENAME)
    if JSONData[' Same_dir '] == True:
        passedScript = os.path.join(output, "PASSED")
        failedScript = os.path.join(output, "FAILED")
        if not os.path.isdir(passedScript):
            os.mkdir(passedScript)
        if not os.path.isdir(failedScript):
            os.mkdir(failedScript)
        if passed == "PASSED":
            handler = logging.handlers.RotatingFileHandler(os.path.join(output, passedScript, LOG_FILENAME),
                                                           backupCount=int(JSONData[' Max_log_files ']) - 1)
        else:
            if passed == "FAILED":
                handler = logging.handlers.RotatingFileHandler(os.path.join(output, failedScript, LOG_FILENAME),
                                                               backupCount=int(JSONData[' Max_log_files ']) - 1)

    handler = logging.handlers.RotatingFileHandler(os.path.join(output, failedScript, LOG_FILENAME),
           backupCount=int(JSONData[' Max_log_files ']) - 1)
    if JSONData[' Same_dir '] == False:
       handler = logging.handlers.RotatingFileHandler(os.path.join( LOG_FILENAME))
    # This is a stale log, so roll it
    my_logger.addHandler(handler)
    if needRoll:

        # Add timestamp
        my_logger.debug('---------\nLog closed on %s.\n---------\n' % time.asctime())
        # Roll over on application start
        my_logger.handlers[0].doRollover()
    # Add timestamp
    my_logger.debug('---------\nLog started on %s.\n---------\n' % time.asctime())
    # Log The Dictionary Result
    for key, value in ResultDict.items():
        my_logger.debug(f'{key} : {value}')


def csv(ResultDict):
    import csv
    count=0
    for value in range(len(Commands.Passed)):
        if Commands.Passed[value] == 1:
            count += 1
    if count == len(Commands.Passed):
        passed = "PASSED"
    else:
        passed = "FAILED"

    filename = f'Output{passed}.csv'
    a_file = open(os.path.join(output, filename), "w")
    writer = csv.writer(a_file)
    for key, value in ResultDict.items():
        writer.writerow([key, value])
    a_file.close()


ReadScript()
JSONData = ParseJSON()
if JSONData[' output '] == "Log":
    Logging(Commands.Result)
else:
    if JSONData[' output '] == "csv":
        csv(Commands.Result)
        