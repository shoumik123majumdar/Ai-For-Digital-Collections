import os
from datetime import datetime
import csv

class Logger:
    """
    Generates logs
    """
    def __init__(self, log_dir=''):
        """
        Initializes the Logger instance.
        :param log_dir: Directory to store logs.
        """
        self.log_dir = log_dir
        if not os.path.isdir(log_dir):
            raise FileNotFoundError(f"No such directory exists: {log_dir}")


    def generate_log(self, log_file_name):
        """
        Generates a log file based on the log_file_name in the Logs directory
        :param log_file_name: Name of the log file to be created
        :return: The path of the generated log file
        """
        log_file_csv = os.path.join(self.log_dir, f'{log_file_name}')

        # Create the log file with the header
        with open(log_file_csv, 'w', newline='') as log_file:
            log_file.write("File Name,Process Start Time,Process End Time,Error Message\n")

        return log_file_csv

    def append_entry(self, log_file_path, file_name, process_start_time, process_end_time="",error_message=""):
        """
        Appends a new log entry to the existing log file if the image processing was successful
        :param log_file_path: The path of the log file.
        :param file_name: Name of the file being processed.
        :param process_start_time: The start time of the process.
        :param process_end_time: The end time of the process.
        :param error_message: Error message if it occurs
        :return: None, the log file is altered in place.
        """
        with open(log_file_path, 'a', newline='') as log_file:
            writer = csv.writer(log_file)
            if error_message == "":
                print(f'Image file at {file_name} was processed successfully')
            else:
                print('Image file at {file_name} encountered an error while processing')
            writer.writerow([file_name, process_start_time, process_end_time, error_message])


