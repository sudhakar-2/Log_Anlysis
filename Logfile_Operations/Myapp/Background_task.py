from apscheduler.schedulers.background import BackgroundScheduler
import re,io,csv
from django.http import HttpResponse
from django.conf import settings


import csv
import re
import io
import os

def log_to_csv():
    print("Calling background task")
    file_path=settings.CSV_FILE_PATH
    # file_path="C:\\Users\\Crimson innovative\\Desktop\\Log Analysis Files\\Logfile_Operations-6-9-24\\Logfile_Operations-6-9-24\\Logfile_Operations\\LogFile_Container\\Converted_Data.csv"
    # Define the log file path (update as needed)
    log_file_path=settings.LOG_FILE_PATH
    # log_file_path = 'C:\\Users\\Crimson innovative\\Desktop\\Log Analysis Files\\Logfile_Operations-6-9-24\\Logfile_Operations-6-9-24\\Logfile_Operations\\LogFile_Container\\logdata.log'

    # Define a list of substrings to check for
    substring_list = ["logPsm4Paramters", "TrdRobot", "EPU on-chip Temperature (Celsius): 23.00"]

    # Define a function to parse each line of the log file
    def parse_log_line(log_line):
        # Regex to capture datetime and the entire log line after INFO
        regex = r"(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - Log:.*? (?P<log_level>INFO|WARNING|ERROR) (?P<event_template>.*)"

        match = re.match(regex, log_line)
        if match:
            datetime_str = match.group('datetime')
            event_template = log_line
            
            # Find substring from the predefined list
            substring = next((sub for sub in substring_list if sub in event_template), '')

            return datetime_str, event_template, substring
        return None, None, None

    # Create or overwrite the CSV file
    try:
        file_exists = os.path.isfile(file_path)
        with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the header only if the file is empty or doesn't exist
            if not file_exists or os.stat(file_path).st_size == 0:
                csv_writer.writerow(['Datetime', 'Event_Template', 'Search_string'])
            
            # Read log file, parse it, and write to CSV
            with open(log_file_path, 'r') as log_file:
                for line in log_file:
                    datetime_str, event_template, substring = parse_log_line(line)
                    if datetime_str:
                        csv_writer.writerow([datetime_str, event_template, substring])

        # Truncate the log file to avoid duplicate data
        with open(log_file_path, 'w') as log_file:
            log_file.truncate(0)
        
    except FileNotFoundError:
        print(f"Log file not found: {log_file_path}")
    except IOError as e:
        print(f"Error writing to file {file_path}: {e}")

    print(f"CSV data has been written to {file_path}")
    # with open(log_file_path, 'w') as log_file:
    #         log_file.truncate(0)

# Example usage


    