#!/usr/bin/env python

# Download Everything
# Download URLs from text file(s)
# version 2.92

import logging
import os
import time
import glob
import urllib

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
pid = os.getpid()
errorlogname = "de-" + str(pid) + "-error.log"
logging.basicConfig(format='%(asctime)s %(message)s', filename=errorlogname, level=logging.ERROR)

# Can filter Using this.
textFiles = glob.glob("*-urls.txt")
print "Using Files:\t" + str(textFiles).strip('[]')

# Replace this with something that reads all .txt files into the list
for textFile in textFiles:
    with open(textFile) as f:
        urls.extend(f.read().splitlines())

for url in urls:
    if url == "\n":
        print(url + " is newline.")
        break
    print url

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
        category = "unknown"

    # loop through them and prepend the domain name and folder
    logging.info("Processing " + filename)
    
    # Check if category directory exists.
    if not os.path.isdir(category):
        # If not create it
        os.makedirs(category)

    if os.path.isfile( category + "/" + filename ):
        # File does not exist. So Download it.
        print(filename + " already exists.")
        logging.warning(filename + " Already Exists.")
        filesSkipped += 1
    else:
        print(filename)
        try:
            resp = urllib.urlopen(url)
        except URLError as e:
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
                print "Error: " + filename + " not found on server."
                errorOccured = True
            else:
                with open( category + "/" + filename, "w") as newfile:
                    newfile.write(resp.read())
                    logging.info(filename + ": OK.")
                    print "Processing " + filename + ": OK."
                    filesWritten += 1

print "\t\t\t-- Finished --\n\tFiles Written:\t\t" + str(filesWritten) + "\t\tFiles Skipped:\t" + str(filesSkipped)

if errorOccured:
    print "\t\t\t-- An error(s) occurred while downloading file. --"
    print "\t\tPlease check " + errorlogname + " for more information."

