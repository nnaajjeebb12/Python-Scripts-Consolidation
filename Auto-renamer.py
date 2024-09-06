"""
The purpose of this script is to automate the process where in the machine will output a raw file,
and then convert it to a format readable by the map parser
"""


import os
from datetime import datetime
from configparser import ConfigParser, NoSectionError, NoOptionError

def ReadIni():
    """
    Read the Ini file where the paths are stored

    Returns:
        Input (str): Path to the input folder
        Output (str): Path to the output folder
        Log (str): Path to the log folder
        ErrorFolder (str): Path to the error folder
        isDelLine (bool): boolean flag whether to delete line or not
    Raises:
        FileNotFoundError: If the INI file does not exist.
        NoSectionError: If a required section is missing in the INI file.
        NoOptionError: If a required option is missing in the INI file.
        ValueError: If the value for the deletion flag is not a valid boolean.    
    """
    
    try:
        Input = Output = Log = ""
        isDelLine = False
        configRead = ConfigParser()
        configRead.read('ini\\Config.ini')
        Input = configRead.get("FOLDER_PATH", 'Input_Folder')
        Output = configRead.get("FOLDER_PATH", 'Output_Folder')
        Log = configRead.get("FOLDER_PATH", 'Log_Folder')
        ErrorFolder = configRead.get("FOLDER_PATH", 'Error_Folder')
        isDelLine = configRead.get("DEL_LINE", "DEL")
        
    except FileNotFoundError:
        print("Ini File does not exist")
        raise        
    except NoSectionError as e:
        error = f"{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}: Missing section in INI file: {e}\n"
        writeLogs(Log, error)
        raise
    except NoOptionError as e:
        error = f"{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}: Missing option in INI file: {e}\n"
        writeLogs(Log, error)
        raise
    except ValueError as e:
        error = f"{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}: Invalid value in INI file: {e}\n"
        writeLogs(Log, error)
        raise
    return Input, Output, Log, isDelLine, ErrorFolder

def ProcessMap(InputFolder, OutputFolder, Log, Error, DeleteLine):    
    """
    Process Input files with Wafer_Batch.### format to rename to a Wafer-ID.stif format then moves to OutputFolder 
    Deletes extra line if isDelLine is True

    Arguments:
        InputFolder (str): path of the input folder
        OutputFolder (str): path of the output folder
        Log (str): path of the log folder
        Error (str): path of the error folder
    Raises:
        OSError: If there are issues with renaming, moving or checking if the file exists
        Exception: If there are any unexpected errors occured
    """
    try:
        for filename in os.listdir(InputFolder):
            f =  os.path.join(InputFolder, filename)
            ext = filename.partition('.')
            
            if DeleteLine:
                if not Delete_line(f, Log, Error):
                    return

            if ext[-1].isnumeric():      
                
                LOT, READER = readFile(f)
                
                new_name = filename.replace(ext[0],READER.partition("\n")[0])
                new_name = new_name.replace(ext[-1],'stif')
                new_path = os.path.join(OutputFolder,new_name)
                
                if os.path.exists(new_path):
                    os.remove(new_path)
                    
                os.rename(f,new_path)
                
                logContent = f"{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}: Succesfully renamed {filename} to {new_name}\n"
                writeLogs(Log, logContent)
                
    except OSError as e:
        error_msg = f"{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}: OSError Occured [{e}]\n"
        writeLogs(Log)
        raise
    except Exception as e:
        error_msg = f"{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}: Unexpected Error Occured [{e}]\n"
        raise

def writeLogs(logPath,logContent):
    """
    Write logs or create a log file depending on the day
    Log format is always day-Month-Year standard ST Format
    

    Args:
        logPath (str): path to the log file
        logContent (str): text thta saves 
    """    
    if not os.path.exists(logPath):
        os.makedirs(logPath)

    today_date = datetime.now().strftime('%d-%b-%Y')
    log_fileName = f"{today_date}.log"

    logFile_path = os.path.join(logPath,log_fileName)
    if not os.path.isfile(logFile_path):
        with open(logFile_path, 'w') as file:
            file.write(logContent)
    else:
        with open(logFile_path, 'a') as file:
            file.write(logContent)

def readFile(filePath):
    """
    Read map file based on the file path from the ProcessMap function

    Args:
        filePath (str): full filepath of the map file

    Returns:
        LOT (str): Returns the value of the LOT from the map
        READER (str): Returns the value of the READER from the map
    """
    with open(filePath,'r') as file:
        for each in file:
            if each.__contains__('LOT'):
                LOT = each.partition('\t')[-1]
            elif each.__contains__('READER'):
                READER = each.partition('\t')[-1]
    return LOT, READER

def Delete_line(filePath, Log, Error):
    
    """
    Deletes the extra line

    Returns:
        _type_: _description_
    """
    
    fileName = os.path.basename(filePath)
    
    with open(filePath,'r') as file:
        lines = file.readlines()
    edate_index = None
    
    for i, line in enumerate(lines):
        if 'MERGEDATE' in line:
            pass
        elif 'EDATE' in line:
            edate_index = i
            break
        
    if edate_index is None:
        logContent = f"{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}: EDATE not found in the STIF map {fileName}\n"
        Error_Path = os.path.join(Error, fileName)
        if os.path.exists(Error_Path):
            os.remove(Error_Path)
        writeLogs(Log, logContent)                      
        os.rename(filePath,Error_Path)
        return False
    
    for i in range(edate_index - 1, -1, -1):
        if lines[i].strip():
            del lines[i +1:edate_index]
            break
    with open(filePath,'w') as file:
        file.writelines(lines)
    return True

Input,Output,Log,isDelLine,ErrorFolder = ReadIni()
ProcessMap(Input, Output, Log, ErrorFolder, isDelLine)
