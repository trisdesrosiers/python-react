#!/usr/bin/python

# Standard imports
import logging
import logging.handlers
import os
import pytz
from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self, file_name: str):
        self.ignored_substrings = ['psql.', 'config.', 'operations.', 'requests.', 'models.']

        self.logger = logging.getLogger(file_name)
        self.logger.setLevel(logging.DEBUG)
        
        if self.logger.handlers:
            return
            
        # Setup log file
        save_name = file_name
        for substring in self.ignored_substrings:
            save_name = save_name.replace(substring, '')
        
        # log_dir = Path(os.path.dirname(os.path.abspath(__file__))) / "logs"
        log_dir = Path("/app/psql/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure handlers
        file_handler = logging.FileHandler(log_dir / f"{save_name}.txt")
        # console_handler = logging.StreamHandler()

        # Set format and add handlers
        eastern = pytz.timezone('America/New_York')
        
        # Custom formatter that uses Eastern Time
        class EasternFormatter(logging.Formatter):
            def formatTime(self, record, datefmt=None):
                dt = datetime.fromtimestamp(record.created, eastern)
                if datefmt:
                    return dt.strftime(datefmt)
                else:
                    return dt.strftime('%Y-%m-%d %H:%M:%S')
        
        formatter = EasternFormatter("[ %(asctime)s ] - %(levelname)s - %(message)s")
        
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        # console_handler.setFormatter(formatter)
        # self.logger.addHandler(console_handler)
    
    def get(self):
        return self.logger

