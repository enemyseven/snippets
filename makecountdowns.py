#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: FFmpeg Image Generation and Overlay
Author: Cody Hill
Date Created: April 2, 2021
Last Modified: April 2, 2021
Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt
(C) 2021 Cody Hill
"""
import time
import os
import subprocess
import csv
from watermark import make_watermark

VERSION = '0.0.2'

# MARK: Variables

# Directories
# It assumes these paths exist prior to running
ffmpeg = "./ffmpeg"
watermarkPath = "./watermark-images/"
outputPath = "./output/"

def setup():
        # Check to see if directory exists.
    if not os.path.isdir("watermark-images"):
        # If not create it.
        os.makedirs("watermark-images")
    if not os.path.isdir("output"):
        # If not create it.
        os.makedirs("output")
        
def processName(input):
    if input[-1] == 's':
        if input[-2] == 's':
            return input + "\'s"
        else:
            return input +"\'"
    else:
        return input + "\'s"

def main():
    print("Starting individual data work...")
    with open('example.csv', newline = '') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            
            name = row['Name_for_Video_Overlay']
            winner_id = row['Winner_ID']
            
            wm_text = processName(name)
            wm_filepath = watermarkPath + winner_id + ".png"
            
            make_watermark(wm_text, wm_filepath)
            
            outputFile = outputPath + winner_id + "-countdown.mp4"
            
            filter = '"fade=in:st=0:d=1:alpha=1,fade=out:st=1820:d=1:alpha=1[ovr];[0][ovr]overlay"'
                       
            execute = ffmpeg + " -i \"A-sixty-to-thirty-countdown-30p.mp4\" -loop 1 -t 1822 -i " + wm_filepath + " -filter_complex \"[1:v]format=rgba,fade=in:st=0:d=1:alpha=1,fade=out:st=1820:d=1:alpha=1 [ovr]; [0][ovr] overlay\" -codec:a copy " + outputFile + " -y"
            
            try:
                subprocess.run(execute, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(e.output)
            
            # Clean up temp user files here.
            
    # Clean up global cache files here.


if __name__ == "__main__":
    setup()
    #xecute only if run as a script
    # Make note of time
    start = time.time()
    main()
    end = time.time()
    total = str(end - start)
    print("Took: " + total)
