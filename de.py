#!/usr/bin/env python3
"""
# Name: Download Everything
# Description: Download files from URLs contained in text files.
# Version: 3.02
# Last Modified: 2021.06.30
"""

import argparse
import logging
import os
import sys
import datetime
import glob
import urllib.request
import urllib.error
import socket

def get_extension(filename):
    basename = os.path.basename(filename)  # os independent
    ext = '.'.join(basename.split('.')[1:])
    return '' + ext if ext else None

def download_file(sourceURL, destinationPath):
    try:
        resp = urllib.request.urlopen(sourceURL)
    except urllib.error.HTTPError as e:
        if hasattr(e, 'reason'):
            logging.error("Error: Failed to reach the server.\n\t\tRef: " + sourceURL)
            print('\t\tFailed to reach the server.')
            print('\t\tReason: ', e.reason)
        elif hasattr(e, 'code'):
            logging.error("Error: Server couldn't fulfill the request.\n\t\tRef: " + sourceURL)
            print('\t\tThe server couldn\'t fulfill the request.')
            print('\t\tError code: ', e.code)
        return False
    except urllib.error.URLError as e:
        logging.error("Error: " + str(e.reason) + "\n\t\tRef: " + sourceURL)
        print("\t\tURLError\n\t\t" + str(e.reason))
        return False
    except socket.timeout:
        logging.error("Error: socket timeout\n\t\tRef: " + sourceURL)
        print("\t\Error: socket timeout\n\t\t")
        return False
    else:
        if resp.getcode() != 200:
            logging.error("Error: Not found on server.\n\t\tRef: " + sourceURL)
            print("\t\tError: File not found on server.")
            return False
        else:
            with open( destinationPath, "wb") as newfile:
                newfile.write(resp.read())
                logging.info(destinationPath + ": OK.")
                print("\t\tSuccessfully downloaded.")
                return True

def process_urls(textFiles):
    # Setting script call time
    callTime = datetime.datetime.today()

    # statistical variables
    errorOccured = False
    filesWritten = 0
    filesSkipped = 0
    filesNotFound = 0

    # Define Empty urls list
    urls = []
    category = ""

    # Setup logging information
    formattedTime = callTime.strftime("%Y.%m.%d - %H.%M.%S")
    errorlogname = "de-error-" + formattedTime + ".log"
    logging.basicConfig(format='%(asctime)s %(message)s', filename=errorlogname, level=logging.ERROR)

    # Display what files are being used.
    print("Using Files:\t" + str(textFiles).strip('[]') + "\n")

    # Read and files into a list to process
    for textFile in textFiles:
        with open(textFile) as f:
            urls.extend(f.read().splitlines())

    for url in urls:
        # Silence Empty line errors.
        if url.strip() == "":
            #print("Error: Encounted empty line")
            break

        filename = url[url.rfind('/') + 1:]
        fileExtension = get_extension(filename)

        # If you want to separate stuff by file extension.
        if fileExtension == None:
            category = 'unknown'
        else:
            category = fileExtension.lower()

        # loop through them and prepend the domain name and folder

        # Check if category directory exists.
        if not os.path.isdir(category):
            # If not create it
            os.makedirs(category)

        print("\nProcessing:\t" + filename)

        if os.path.isfile( category + "/" + filename ):
            # File already exists. So skip it.
            print("\t\tStatus: file already exists.")
            filesSkipped += 1
        else:
            if (download_file(url, category + '/' + filename)):
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

def main():
    parser = argparse.ArgumentParser(prog='de', description='Download all URLs in text files.')
    parser.add_argument(
    'files',
    type=str,
    nargs='*',
    help='Text files to process')

    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    process_urls(args.files)

if __name__ == "__main__":
    main()
