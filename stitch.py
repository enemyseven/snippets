#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: FFmpeg Concatenate Script
Author: Cody Hill
Date Created: February 23, 2021
Last Modified: February 23, 2021
Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt
(C) 2021 Cody Hill
"""
import time
import os
import subprocess
import csv

VERSION = '0.0.5'

# MARK: Variables

# Data Sources
sourceCSV = 'example.csv'
sourceCommonFiles = 'common_files.txt'

# FFMPEG executable
ffmpeg = "./ffmpeg"

# Directories
uniquePath = "./unique/"
cachePath = "./cache/"
commonPath = "./common/"
outputPath = "./output/"

# MARK: Functions

def setup():
    if not os.path.isdir(outputPath):
        os.makedirs(outputPath)

def processVideo(input):
    pre, ext = os.path.splitext(input)
    cachename = pre + ".ts"
    if not os.path.isfile(cachename):
        execute = [
            ffmpeg,
            '-i',
            input,
            '-c',
            'copy',
            '-ar',
            '48000',
            '-bsf:v',
            'h264_mp4toannexb',
            '-f',
            'mpegts',
            f'{cachename}',
            '-y'
        ]
        try:
            subprocess.run(execute, check=True)
        except subprocess.CalledProcessError as e:
            print("Early exit due to error.")
            exit()
            
def isCached(input):
    pre, ext = os.path.splitext(input)
    cachename = pre + ".ts"

    if os.path.isfile(cachename):
        return True
    else:
        return False

def purgeTemporaryFiles(directory):
    commonFiles = []
    # Get a list of files used in multiple videos
    with open(sourceCommonFiles) as f:
        commonFiles.extend(f.read().splitlines())
        
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".ts")]

    for file in filtered_files:
        # Check for common files in the unique directory in case "someone" just dumped everything in one place...
        if file in commonFiles:
            continue
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

def makeVideos():
    # Make note of time
    start = time.time()

    print("Starting individual data work...")
    with open(sourceCSV, newline = '', encoding='utf-8-sig') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            outputStack = []
            buildString = 'concat:'
            
            outputFile = outputPath + row['Winner_ID'] + "_stitched.mp4"
            
            outputStack.append(uniquePath + row['Section_1']) # Countdown
            outputStack.append(commonPath + row['Section_2']) # Common Entertainment
            outputStack.append(uniquePath + row['Section_3']) # Manager Video
            outputStack.append(commonPath + row['Section_4']) # Show (full or intro)
            # !!! ONLY IF AVAILABLE !!!
            if row['Section_5']:
                outputStack.append(uniquePath + row['Section_5']) # Thank You Video
            if row['Section_6']:
                outputStack.append(commonPath + row['Section_6']) # Outro
            
            outputStack.append(commonPath + row['Section_7']) # Closing Video
            
            # Process Videos
            for video in outputStack:
                if isCached(video):
                    print("\tVideo Already Cached.")
                else:
                    print("\tCreating Video Cache")
                    processVideo(video)
                
                pre, ext = os.path.splitext(video)
                buildString += pre + ".ts|"
            buildString = buildString[:-1]
            
            execute = [
                ffmpeg,
                '-fflags',  # necessary to ensure that the
                '+genpts',  # concatenated audio segments
                '-async',   # will switch over at the .
                '1',        # same time as the video segment
                '-i',
                f'{buildString}',
                '-c',
                'copy',
                '-bsf:a',
                'aac_adtstoasc',
                outputFile,
                '-y'
            ]
            
            try:
                subprocess.run(execute, check=True)
            except subprocess.CalledProcessError as e:
                print(e.output)
            
            purgeTemporaryFiles(uniquePath)
            
    # Clean up global cache files here.
            
    # Output Time Spent
    end = time.time()
    totalTime = end - start
    print("--- Complete ---")
    print("Total time: " + str(totalTime))


def main():
    setup()
    makeVideos()

if __name__ == "__main__":
    main()
