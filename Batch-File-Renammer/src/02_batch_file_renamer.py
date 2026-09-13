#Setup
import os
import logging
import time
from datetime import datetime
from datetime import date
logging.basicConfig(
    filename= "Automation.log",
    level= logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(message)s"
)
run_date= date.today()
source_folder= "files"
start_time= time.time()
start_datetime= datetime.now()
success_count= 0
failed_count= 0
total_files= 0
count=1
count=1
prefix= input(f"Enter a file prefix: ")
count= int(input(f"Enter a starting number: "))
rename_list= []
for root,dirs,files in os.walk(source_folder):
    for filename in files:
        name,extension= os.path.splitext(filename)
        source_path= os.path.join(root,filename)
        new_filename= f"{prefix}_{count:03}{extension}"
        destination_path = os.path.join(root, new_filename)
        duplicate_counter=1
        base_name= f"{prefix}_{count:03}"
        while os.path.exists(destination_path):
            new_filename= f"{base_name}({duplicate_counter}){extension}"
            destination_path= os.path.join(root,new_filename)
            duplicate_counter+=1
        file_data= {
            "source_path": source_path,
            "destination_path": destination_path,
            "filename": filename,
            "new_filename": new_filename
        }
        rename_list.append(file_data)
        count+=1
for file_data in rename_list:
    print(f"{file_data['filename']}-> {file_data['new_filename']}")
user_choice= input(f"Do you want to rename all file? (y/n)").upper()
if user_choice== "Y":
    for file_data in rename_list:
        total_files+=1
        try:
            os.rename(file_data["source_path"],file_data["destination_path"])
            logging.info(f"File renamed successfully: {file_data['filename']}->{file_data['new_filename']}")
            print(f"File renamed successfully: {file_data['filename']}->{file_data['new_filename']}")
            success_count+=1
        except FileNotFoundError:
            logging.error(f"Failed to rename file: {file_data['filename']} not found ")
            print(f"Failed to rename file: {file_data['filename']} not found")
            failed_count+=1
        except PermissionError:
            logging.error(f"Acess denied Yto the requested file: {file_data['filename']}")
            print(f"Access denied to the requested  file: {file_data['filename']} ")
            failed_count+=1
elif user_choice== "N":
        print("Renaming Cancelled by user")
        exit()
else:
    print("Invalid input")        
        
end_time= time.time()
end_datetime= datetime.now()
execution_time= end_time-start_time
with open ("Batch_renamer.txt","w") as report:
    report.write("================================\n")
    report.write("Batch_renamer v2.1\n")
    report.write("================================\n")
    report.write(f"Run date: {run_date}\n")
    report.write(f"Start Time: { start_datetime.strftime('%d %m %Y %H:%M:%S')}\n")
    report.write(f"End Time: { end_datetime.strftime('%d %m %Y, %H:%M:%S')}\n")
    report.write(f"Execution Time: {execution_time:.3f} seconds\n")
    report.write(f"Source Folder: {source_folder}\n")
    report.write(f"Total Files Processed: {total_files}\n")
    report.write(f"Renamed Files: {success_count}\n")
    report.write(f"Failed Files: {failed_count}\n")







