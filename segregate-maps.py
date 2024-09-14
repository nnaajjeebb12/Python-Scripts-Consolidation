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
    if os.path.exists("config.ini"):
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
    return storeInput, storeProcessOutput, storeProcessName, storeNonProcess

def segregate(store_input, store_process_output, store_process_name, store_non_process):
    inputFiles = os.listdir(store_input)
    prodFiles = os.listdir(store_process_name)
    
    for inputFile in inputFiles:
        productCode = None
        inputFilePath = os.path.join(store_input, inputFile)
        
    with open(inputFilePath, encoding="cp1252") as file:
        lines =  file.readlines()
        
    try:
        for i, line in enumerate(lines):
            if "PRODUCT\t" in line:
                product_store = line[8:].strip()
            elif "EDATE" in line:
                lines[i] = f"EDATE\t{datetime.now().strftime('%Y-%m-%d')}\n"
            elif "ETIME" in line:
                lines[i] = f"ETIME\t{datetime.now().strftime('%H:%M:%S')}\n"
                # Update the file after modifications
                with open(input_file_path, "w", encoding="cp1252") as file:
                    file.writelines(lines)
                break
    except Exception as e:
        continue
    
    try:        
        if product_store:
            found_prod = False
            for prod_file in prod_files:
                if prod_file == product_store:
                    shutil.move(input_file_path, os.path.join(store_process_output, input_file))
                    found_prod = True
                    break
            if not found_prod:
                shutil.move(input_file_path, os.path.join(store_non_process, input_file))
    except Exception as e:
        continue
        
storeInput, storeProcessOutput, storeProcessName, storeNonProcess = ReadIni()
segregate(storeInput, storeProcessOutput, storeProcessName, storeNonProcess)

