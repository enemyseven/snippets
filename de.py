#!/usr/bin/env python3
"""
# Name: Download Everything
# Description: Download URLs from text file(s) containing URLs
# Version: 2.93
# Last Modified: 2021.03.24
"""

import logging
import os
import time
import glob
import urllib.request
import urllib.error

# Setting script call time
callTime = time.time()

# runtime variables
errorOccured = False
filesWritten = 0
filesSkipped = 0

# Define Empty urls list
urls = []
category = ""

# Setup logging information
# Get current Process ID for error log
# Maybe date and time would be better than pid
pid = os.getpid()
errorlogname = "de-" + str(pid) + "-error.log"
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
    logging.info("Processing " + filename)
    
    # Check if category directory exists.
    if not os.path.isdir(category):
        # If not create it
        os.makedirs(category)

    print("Processing: " + filename)
            
    if os.path.isfile( category + "/" + filename ):
        # File does not exist. So Download it.
        print("\tStatus: file already exists.")
        logging.warning("Warning: " + filename + " already Exists.")
        filesSkipped += 1
    else:
        try:
            resp = urllib.request.urlopen(url)
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                logging.error("Error: Failed to reach the server for " + filename)
                print('Failed to reach the server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                logging.error("Error: Server couldn't fulfill the request for "+ filename)
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        else:
            if resp.getcode() != 200:
                logging.error("Error: " + filename + " Not found on server.")
                print("\tError: " + filename + " not found on server.")
                errorOccured = True
            else:
                with open( category + "/" + filename, "wb") as newfile:
                    newfile.write(resp.read())
                    logging.info(filename + " OK.")
                    print("\tStatus: Success")
                    filesWritten += 1

print("\n\t\t\t-- Finished --\n\tFiles Written:\t\t" + str(filesWritten) + "\t\tFiles Skipped:\t" + str(filesSkipped))

if errorOccured:
    print("\t\t\t-- An error(s) occurred while downloading file. --")
    print("\t\tPlease check " + errorlogname + " for more information.")
