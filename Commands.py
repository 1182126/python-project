import glob
import os
import shutil
from os import listdir
from os.path import join, isfile




class Commands:
    Result = {}
    Passed = []

    @staticmethod
    def getCommand(CommandType, ReqList, JSONData, Index):
        if (CommandType == 'Grep'):
            PASS = GrepCommand.GrepDir(ReqList[0], ReqList[1], Index)
            Commands.Passed.append(PASS)
        if (CommandType == 'Mv_last'):
            PASS = MvCommand.MoveDef(ReqList[0], ReqList[1], Index)
            Commands.Passed.append(PASS)
        if (CommandType == 'Categorize'):
            PASS = CategorizeCommand.CatDef(ReqList[0], JSONData[' Threshold_size '], Index)
            Commands.Passed.append(PASS)


# check if a given file is within a specific directory (including its subdirectories).
class GrepCommand(Commands):
    @staticmethod
    def GrepDir(fileName, Dir, Index):
   #     print("Executing Grep Command . . .")
        PASSED = 0
        if (os.path.isdir(Dir)):
            found = 0
            onlyfiles = [f for f in listdir(Dir) if isfile(join(Dir, f))]
            # Search In Files
            if len(onlyfiles) == 0:
                print("Empty Dir")
                Commands.Result[f'Line- {Index + 1}'] = [False]
                PASSED = 1  # Command Passed Execution
            for i in range(len(onlyfiles)):
                onlyfiles[i] = os.path.splitext(onlyfiles[i])[0]
                if onlyfiles[i] == fileName:
                    found = 1
                    print("Successfully Found", fileName, " in ", Dir, " Directory! ")
                    Commands.Result[f'Line- {Index + 1}'] = [True]
                    print(Commands.Result[f'Line- {Index + 1}'], f'Line- {Index + 1}')
                    PASSED = 1
                    break

            if (found == 0):
                SubDir = [d for d in os.listdir(Dir) if os.path.isdir(os.path.join(Dir, d))]
                for i in range(len(SubDir)):
                    New = join(Dir, SubDir[i])
                    onlyfiles = [f for f in listdir(New) if isfile(join(New, f))]
                    for i in range(len(onlyfiles)):
                        onlyfiles[i] = os.path.splitext(onlyfiles[i])[0]
                        if onlyfiles[i] == fileName:
                            print("Successfully Found", fileName, "file in", Dir, "Directory! ")
                            Commands.Result[f'Line- {Index + 1}'] = [True]
                            PASSED = 1
                            return PASSED
                    Commands.Result[f'Line- {Index + 1}'] = [False]
                    PASSED = 1
        else:
            Commands.Result[f'Line- {Index + 1}'] = [False]
            print("NON VALID DIRECTORY")
            PASSED = 0
        return PASSED


# Get The Recently Modified File From The Specified Directory
class MvCommand(Commands):
    @staticmethod
    def MoveDef(src_directory, des_directory, Index):
    #    print("Executing Mv_last Command . . .")
        if (os.path.isdir(src_directory) and os.path.isdir(des_directory)):
            files_path = os.path.join(src_directory, '*')
            files = sorted(
                glob.iglob(files_path), key=os.path.getmtime, reverse=True)
            if len(files) != 0:
                print(files[0])
                Recent_file = files[0]
                # Move The Recently Modified File To The Specified Directory
                try:
                    shutil.move(Recent_file, des_directory)
                    print(f"The Recent File {Recent_file} Is Moved to ", des_directory, " Successfully")
                    Commands.Result[f'Line- {Index + 1}'] = [True]
                    passed = 1
                except shutil.Error:
                    print("Can't Move")
                    passed = 0
                    Commands.Result[f'Line- {Index + 1}'] = [False]
            else:
                Commands.Result[f'Line- {Index + 1}'] = [False]
                print("Dir is Empty")
                passed = 1
        else:
            passed = 0
            Commands.Result[f'Line- {Index + 1}'] = [False]
            print("NON VALID DIRECTORY")
        return passed


class CategorizeCommand(Commands):
    @staticmethod
    def CatDef(dir, threshold_size, Index):
        print("Executing Categorize Command . . .")
        passed = 0
        if (os.path.isdir(dir)):
            threshold_size = (int)(threshold_size[:len(threshold_size) - 2]) * 1024
            # Make BiggerThan Directory
            global onlyfiles
            bigdir = os.path.join(dir, "BiggerThan")
            try:
                os.mkdir(bigdir)
            except OSError:
                print("Creation of the directory %s failed" % bigdir)
            else:
                print("Successfully created the directory %s " % bigdir)
            # Make LessThan Directory
            lessdir = os.path.join(dir, "LessThan")
            try:
                os.mkdir(lessdir)
            except OSError:
                print("Creation of the directory %s failed" % lessdir)
            else:
                print("Successfully created the directory %s " % lessdir)
            # Print all the files within the specific directory
            onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
            if len(onlyfiles) == 0:
                print("No files in the specified")
                Commands.Result[f'Line- {Index + 1}'] = [False]

            for i in range(len(onlyfiles)):
                path = os.path.join(dir, onlyfiles[i])
                size = os.path.getsize(path)
                if size > threshold_size:
                    shutil.move(path, bigdir)
                    Commands.Result[f'Line- {Index + 1}'] = [True]
                    passed = 1
                else:
                    if size < threshold_size:
                        print("Less")
                        Commands.Result[f'Line- {Index + 1}'] = [True]
                        try:
                            shutil.move(path, lessdir)
                            print("Success")
                            Commands.Result[f'Line- {Index + 1}'] = [True]
                            passed = 1
                        except shutil.Error:
                            print("Can't Move")
                            Commands.Result[f'Line- {Index + 1}'] = [False]
                            passed = 0

        else:
            passed = 0
            Commands.Result[f'Line- {Index + 1}'] = [False]
            print("NON VALID DIRECTORY")
        return passed
