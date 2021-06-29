#!/usr/bin/env python3
"""
# Name: Download Everything
# Description: Download files from URLs contained in text files.
# Version: 2.95
# Last Modified: 2021.06.28
"""

import logging
import os
import datetime
import glob
import urllib.request
import urllib.error

def downloadFile(sourceURL, destinationURL):
    try:
        resp = urllib.request.urlopen(sourceURL)
    except urllib.error.HTTPError as e:
        if hasattr(e, 'reason'):
            logging.error("Error: Failed to reach the server.\n\t\t\t\t\tRef: " + sourceURL)
            print('\t\tFailed to reach the server.')
            print('\t\tReason: ', e.reason)
        elif hasattr(e, 'code'):
            logging.error("Error: Server couldn't fulfill the request.\n\t\t\t\t\tRef: " + sourceURL)
            print('\t\tThe server couldn\'t fulfill the request.')
            print('\t\tError code: ', e.code)
        return False
    except urllib.error.URLError as e:
        logging.error("Error: " + e.reason + "\n\t\t\tRef: " + sourceURL)
        print("\t\tURLError\n\t\t" + e.reason)
        return False
    except TimeoutError as e:
        logging.error("Error: TimeoutError\n\t\t\tRef: " + url)
        print("\t\tTimeoutError\n\t\t")
    else:
        if resp.getcode() != 200:
            logging.error("Error: Not found on server.\n\t\t\t\tRef: " + sourceURL)
            print("\t\tError: File not found on server.")
            return False
        else:
            with open( destinationURL, "wb") as newfile:
                newfile.write(resp.read())
                logging.info(destinationURL + ": OK.")
                print("\t\tSuccessfully downloaded.")
                return True


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
        if (decommon.downloadFile(url, category + '/' + filename)):
            filesWritten += 1
        else:
            filesNotFound += 1

print("\n\n\t---- Finished ----")
print("\tWritten:\t" + str(filesWritten))
print("\tSkipped:\t" + str(filesSkipped))
print("\tNot found:\t" + str(filesNotFound))

if errorOccured:
    print("\t-- An error(s) occurred while downloading file. --")
    print("\tPlease check " + errorlogname + " for more information.")
