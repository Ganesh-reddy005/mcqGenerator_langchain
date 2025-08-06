import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%d-%m-%Y__%H:%M:%S')}.log"  #for creating log file name

log_path=os.path.join(os.getcwd(),"logs") #creates a folder names logs, in our current dir
os.makedirs(log_path,exist_ok=True) #only creates folder if does not exist

LOG_FILEPATH=os.path.join(log_path,LOG_FILE) #joins the log folder and log file

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH, #writes log files here instead of terminal
    format='[%(asctime)s] %(lineno)d %(name)s- %(levelname)s- %(message)s' #formatting what should be seen inside newly created log file
)