# Remote fetch test
# File Organizer v2.1 - Dockerize Automation Project
#Setup
import os
import shutil
import logging
import time
from datetime import datetime
counter= {

     "success_count": 0,
     "failed_count": 0,
     "duplicate_count": 0,
     "total_files":0,
     "documents": 0,
     "pictures": 0,
     "music": 0,
     "videos": 0,
     "others": 0,


}
logging.basicConfig(
    filename= "Automation.log",
    level= logging.INFO,
    format= "%(asctime)s| %(levelname)s | %(message)s"
)
source_folder = "/source"
output_folder = "/output"
start_time= time.time()
start_datetime= datetime.now()
def categorize_file(extension):
     if extension in (".pdf",".txt"):
          return "documents"
     elif extension in (".png",".jpg"):
          return "pictures"
     elif extension in (".zip",".exe",".docx"):
          return "others"
     elif extension== ".mp3":
          return "music"
     elif extension== ".mp4":
          return "videos"
     else:
          return "others"
def handle_duplicate(destination_path,destination_folder,name,extension):
     count=1
     is_duplicate= False
     while os.path.exists(destination_path):
        is_duplicate= True
        new_filename= name+ f"({count})"+extension
        destination_path= os.path.join(destination_folder,new_filename)
        count+= 1
     return destination_path,is_duplicate
def update_counter(counter,category):
     counter[category]+=1
def generate_report(
          start_datetime,
          end_datetime,
          execution_time,
          counter
          ):
     with open("automation_report.txt","w") as report:
          report.write("===========================\n")
          report.write("AUTOMATION REPORT\n")
          report.write("===========================\n")
          report.write(f"Start Time: { start_datetime.strftime('%d %m %Y, %H:%M:%S')}\n")
          report.write(f"End Time: {end_datetime.strftime('%d %m %Y, %H:%M:%S')}\n")
          report.write(f"Execution Time: {execution_time:.3f} seconds\n")
          report.write(f"Total Files Processed: {counter['total_files']}\n")
          report.write(f"Successfully Moved: {counter['success_count']}\n")
          report.write(f"Failed Files: {counter['failed_count']}\n")
          report.write(f"Duplicate Files: {counter['duplicate_count']}\n")
          for category in ["documents","pictures","music","videos","others"]:
               report.write(f"{category.title()}: {counter[category]}\n")
     
#File processing
for root,dirs,files in os.walk(source_folder):
     for file in files:
          counter["total_files"]+=1
          source_path= os.path.join(root,file)
          print(source_path)
          name,extension= os.path.splitext(file)
          print(extension)
          category= categorize_file(extension)
          destination_folder= os.path.join (
                         output_folder,
                         category
                         )
          os.makedirs(destination_folder,exist_ok= True)
          destination_path= os.path.join(destination_folder,file)
          destination_path, is_duplicate= handle_duplicate(
               destination_path,
               destination_folder,
               name,
               extension
               )


          try:     
              shutil.move(source_path,destination_path)
              logging.info(f"File {file} moved successfully to {destination_folder}")
              counter["success_count"]+=1
              update_counter(counter,category)
              if is_duplicate:  
               counter["duplicate_count"]+=1

          except FileNotFoundError:
              logging.error(f"Failed to move {file}: file not found error")
              counter["failed_count"]+= 1
             
          except PermissionError:
              logging.error("Acess denied to the requested file")
              counter["failed_count"]+= 1

#Finalization

if not files:
        print("No files found in download folder") 
        logging.info("No files found in downloads folder")
end_datetime= datetime.now()        
end_time= time.time()
execution_time= end_time- start_time

#Report Generation
generate_report(start_datetime,
          end_datetime,
          execution_time,
          counter
          )
