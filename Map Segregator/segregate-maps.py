import os
from datetime import datetime
from configparser import ConfigParser, NoSectionError, NoOptionError

def writeLogs(error_message):
    log_file = os.path.join(os.getcwd(), "Log")
    if not os.path.exists(log_file):
        os.makedirs(log_file)
    logfile_path = os.path.join(log_file, "Logs.log")
    with open(logfile_path, 'a') as log:
        log.write(error_message)

def ReadIni():    
    
    if os.path.exists('Map Segregator/ini'):
        print("INI file found")
    else:
        print("INI file not found")

    try:
        storeInput = storeProcessOutput = storeProcessName = storeNonProcess = ""
        configRead = ConfigParser()
        configRead.read('Map Segregator\\ini\\config.ini')
        storeInput = configRead.get("FOLDER_PATH", 'store_input')
        storeProcessOutput = configRead.get("FOLDER_PATH", 'store_process_name')
        storeProcessName = configRead.get("FOLDER_PATH", 'store_process_output')
        storeNonProcess = configRead.get("FOLDER_PATH", 'store_non_process')
        
    except FileNotFoundError:
        print("Ini File does not exist")
        raise        
    except NoSectionError as e:
        error = f"{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}: Missing section in INI file: {e}\n"
        writeLogs(error)
        raise
    except NoOptionError as e:
        error = f"{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}: Missing option in INI file: {e}\n"
        writeLogs(error)
        raise
    except ValueError as e:
        error = f"{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}: Invalid value in INI file: {e}\n"
        writeLogs(error)
        raise
    
    print(storeInput)
    print(storeProcessOutput)
    print(storeProcessName)
    print(storeNonProcess)
    return storeInput, storeProcessOutput, storeProcessName, storeNonProcess

ReadIni()