# Testing feature branch
import os
APP_ENV= os.getenv("APP_ENV","development")
print(f"Application Enviroment: {APP_ENV}")
import shutil
import logging
import time
from datetime import datetime
from datetime import date
import hashlib
import json
import argparse
parser= argparse.ArgumentParser()
parser.add_argument(
     "--source",
     required= True,
     help= "Path to the source folder"

)
parser.add_argument(
     "--backup",
     required= True,
     help= "Destination to the backup folder"
)
args= parser.parse_args()
source_folder= args.source
backup_folder= args.backup


logging.basicConfig(
    filename= "Automation.log",
    level= logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(message)s"

)
run_date= date.today()
start_time= time.time()
start_datetime= datetime.now()
success_count= 0
failed_count= 0
skipped_count= 0
verified_count= 0
verification_failed_count= 0
files_to_copy= []
files_to_skip= []
new_files=0
updated_files=0
total_files= 0
def calculate_hash(file_path):
     file_hash= hashlib.sha256()
     chunk_size= 4096
     with open (file_path,"rb") as file:
          chunk= file.read(chunk_size)
          while chunk:
               file_hash.update(chunk)
               chunk= file.read(chunk_size)
          return file_hash.hexdigest()
def verify_hash(source_path,destination_path):
     source_hash= calculate_hash(source_path)
     destination_hash= calculate_hash(destination_path)
     if source_hash== destination_hash:
          return True
     else:
          return False
if os.path.isdir(source_folder):
    if not os.path.exists(backup_folder):
        os.mkdir(backup_folder)
else:
    print(f"Source folder not found: {source_folder}")        
for root,dirs,files in os.walk(source_folder):
    for file in files:
        total_files+=1
        source_path= os.path.join(root,file)
        relative_path= os.path.relpath(root,source_folder)
        destination_folder=os.path.join(backup_folder,relative_path)
        destination_path= os.path.join(destination_folder,file)
        os.makedirs(destination_folder,exist_ok=True)
        if os.path.exists(destination_path):
            source_size= os.path.getsize(source_path)
            destination_size=os.path.getsize(destination_path)
            source_time= os.path.getmtime(source_path)
            destination_time= os.path.getmtime(destination_path)
            if source_size== destination_size: 
                if source_time== destination_time:
                    files_to_skip.append((source_path,destination_path))
                    skipped_count+=1
                    continue
        files_to_copy.append((source_path,destination_path)) 
print(f"Files to copy: {len(files_to_copy)}") 
for source_path,destination_path in files_to_copy:
        print(f"Source: {source_path}")
        print(f"Destination: {destination_path}")
print(f"\n Files to skip: {len(files_to_skip)}")
for source_path,destination_path in files_to_skip:
        print(f"Source: {source_path}")
        print(f"Destination: {destination_path}")
user_choice= input(f"Continue backup? (y/n)").upper()   
if user_choice== "Y" :
      for source_path,destination_path in files_to_copy:
            try:
                 shutil.copy2(source_path,destination_path)
                 base_name= os.path.basename(source_path)
                 if verify_hash(source_path,destination_path):
                      verified_count+=1
                      logging.info(f"Hash verified successfully: {base_name}")
                 else:
                      verification_failed_count+=1   
                      logging.error(f"Hash verification failed: {base_name} ")             
                 success_count+=1 
                 logging.info(f"File copied successfully: {base_name}") 
                 print(f"File copied successfully: {base_name}") 
      
            except FileNotFoundError: 
                 logging.error(f"Requested file not found: {base_name}") 
                 print(f"File not found error: {base_name}")
                 failed_count+=1 
            except PermissionError: 
                 logging.error(f"Access denied to the requested file: {base_name}") 
                 print(f"Access denied to the requested file: {base_name}") 
                 failed_count+=1 
            except IsADirectoryError: 
                 logging.error(f"Requested file is a directory: {base_name}") 
                 print(f"Requested file is a directory: {base_name}") 
                 failed_count+=1 
            except OSError as e: 
                 logging.error(f"The following error is : {e}") 
                 print(f"The following error is: {e}") 
                 failed_count+=1    
elif user_choice== "N":
     print("Backup cancelled")
else:
     print(f"Invalid Choice: please Enter Y aur N") 
logging.info("Backup completed")
print("Backup completed")          
end_time= time.time()
end_datetime= datetime.now()
execution_time= end_time-start_time

report_data= {
     "run_info": {
          "run_date": run_date.strftime('%d %m %Y'),
          "start_time": start_datetime.strftime('%d %m %Y %H:%M:%S'),
          "end_time": end_datetime.strftime('%d %m %Y %H:%M:%S'),
          "execution_time": f"{execution_time:.3f} seconds",
          },
          "backup_info": {
               "source_folder": source_folder,
               "backup_folder": backup_folder,
               "backup_type": "Full",
               "verification_algorithm": "SHA-256"
          },
          "statistics": {
               "total_files": total_files,
               "success_count": success_count,
               "failed_count": failed_count,
               "skipped_count": skipped_count,
               "verified_count": verified_count,
               "verification_failed_count": verification_failed_count
          }
}
with open("Smart_backup_report.json","w") as report:
     json.dump(report_data,report,indent=4)


with open ("Smart_backup_utility.txt","w") as report:
    report.write("===============================\n")
    report.write("Smart Backup report\n")
    report.write("===============================\n")
    report.write(f"Run Date: {run_date}\n")
    report.write(f"Start Time: {start_datetime.strftime('%d %m %Y %H:%M:%S')} \n")
    report.write(f"End time: {end_datetime.strftime('%d %m %Y %H:%M:%S')}\n")
    report.write(f"Execution Time: {execution_time:.3f} seconds\n")
    report.write(f"Source Folder: {source_folder}\n")
    report.write(f"Backup Folder: {backup_folder}\n")
    report.write(f"Total Files: {total_files}\n")
    report.write(f"Successfully copied: {success_count}\n")
    report.write(f"Files to copy: {len(files_to_copy)}\n")
    report.write(f"Files to skip: {len(files_to_skip)}\n")
    report.write(f"Failed copies: {failed_count}\n")
    report.write(f"Skipped Files: {skipped_count}\n")
    report.write(f"Verified files: {verified_count}\n")
    report.write(f"Verification failed: {verification_failed_count}")









    

