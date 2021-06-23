#!/usr/bin/env python3
"""
# Name: Download Everything
# Description: Download files from URLs contained in text files.
# Version: 2.95
# Last Modified: 2021.06.23
"""

import logging
import os
import datetime
import glob
import urllib.request
import urllib.error

# Setting script call time
callTime = datetime.datetime.today()

# runtime variables
errorOccured = False
filesWritten = 0
filesSkipped = 0
filesNotFound = 0

# Define Empty urls list
urls = []
category = ""

# Setup logging information
# Get current Process ID for error log
# Maybe date and time would be better than pid
#pid = os.getpid()
formattedTime = callTime.strftime("%Y.%m.%d - %H.%M.%S")
errorlogname = "de-error-" + formattedTime + ".log"
logging.basicConfig(format='%(asctime)s %(message)s', filename=errorlogname, level=logging.ERROR)

# Can filter Using this.
textFiles = glob.glob("*-urls.txt")
print("Using Files:\t" + str(textFiles).strip('[]') + "\n")

# Replace this with something that reads all .txt files into the list
for textFile in textFiles:
    with open(textFile) as f:
        urls.extend(f.read().splitlines())

for url in urls:
    # Silence Empty line errors.
    if url.strip() == "":
        #print("Error: Encounted empty line")
        break

    filename = url[url.rfind('/') + 1:]
    fileExtension = filename[filename.rfind('.') + 1:].lower()
    
    # If you want to separate stuff by file extension.
    if fileExtension == "mp4":
        category = "mp4"
    elif fileExtension == "mov":
        category = "mov"
    elif fileExtension == "jpg":
        category = "jpg"
    elif fileExtension == "jpeg":
        category = "jpeg"
    elif fileExtension == "png":
        category = "png"
    elif fileExtension == "gif":
        category = "gif"
    else:
        category = "other"

    # loop through them and prepend the domain name and folder
    
    # Check if category directory exists.
    if not os.path.isdir(category):
        # If not create it
        os.makedirs(category)

    logging.info("Processing " + filename)
    print("\nProcessing:\t" + filename)
            
    if os.path.isfile( category + "/" + filename ):
        # File does not exist. So Download it.
        print("\t\tStatus: file already exists.")
        logging.warning("Warning: " + filename + " already Exists.")
        filesSkipped += 1
    else:
        try:
            resp = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            if hasattr(e, 'reason'):
                logging.error("Error: Failed to reach the server for " + filename)
                print('\t\tFailed to reach the server.')
                print('\t\tReason: ', e.reason)
            elif hasattr(e, 'code'):
                logging.error("Error: Server couldn't fulfill the request for "+ filename)
                print('\t\tThe server couldn\'t fulfill the request.')
                print('\t\tError code: ', e.code)
            filesNotFound += 1
        except urllib.error.URLError as e:
            logging.error("Error: " + str(e) + "\n\t\t\t\t\tRef: " + url)
            print("\t\tError: Perhaps server does not exist.")
        else:
            if resp.getcode() != 200:
                logging.error("Error: " + filename + " Not found on server.")
                print("\t\tError: " + filename + " not found on server.")
                filesNotFound += 1
                errorOccured = True
            else:
                with open( category + "/" + filename, "wb") as newfile:
                    newfile.write(resp.read())
                    logging.info(filename + " OK.")
                    print("\t\tStatus: Success")
                    filesWritten += 1

print("\n\n\t---- Finished ----")
print("\tWritten:\t" + str(filesWritten))
print("\tSkipped:\t" + str(filesSkipped))
print("\tNot found:\t" + str(filesNotFound))

if errorOccured:
    print("\t-- An error(s) occurred while downloading file. --")
    print("\tPlease check " + errorlogname + " for more information.")
