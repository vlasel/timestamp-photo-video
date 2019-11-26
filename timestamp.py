#!/usr/bin/env venv/bin/python3

""" Restores video and photo file's creation and modification timestamp to the correct value.

For video files uses filename's pattern 'yyyyMMdd_hhmmss'. Adds its duration to timestamp.
For photos an EXIF data, and if not exists the uses filename's pattern.

usage: timestamp.py [File name mask]
"""


import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from moviepy.editor import VideoFileClip


__date__ = "2019-11-20"
__author__ = "Viktor Volisov"
#__copyright__ = "2019, Viktor Volisov"
#__credits__ = "[Viktor Volisov]"
#__license__ = "GPL"
__version__ = "0.0.1"

__description = """Restores video file's creation and modification dates back to the original 
value from filename's pattern 'yyyyMMdd_hhmmss'. Also adds its duration to the modification date.
usage: timestamp.py [File name mask]"""

isVerbose = False


def main(args):
    
    if (not len(args)):
        usage()
        return - 1
    
    if (isVerbose):
        print("args = {0}".format(args))
    
    process_args(args)
    
    # First arg is file or directory path
    path = args[0]

    if not isVerbose:
        print("Update of modification and access time:")

    if (os.path.isfile(path)):
        # Update the file's timestamp
        update_file_timestamp(path)
    elif (os.path.isdir(path)):
        # traverse root directory, and list files
        path = os.path.normpath(path)
        for curr, dirs, files in os.walk(path):
            for file in files:
                path = os.path.join(curr, file)
                update_file_timestamp(path)

        print()
    else:
        print("The path {0} is not file or directory.".format(path))
        usage()
        return -1
            
    
def usage():
    print(__description)
    
    
def process_args(args):
    # Argument '-v' is for 'verbose' mode that means more detailed logging
    if(len(args) > 1 and "-v" in args):
        global isVerbose
        isVerbose = True


def update_file_timestamp(filepath):
    if(isVerbose):
        print('filepath=' + filepath)
    file_stat_before = os.stat(filepath)
     
    new_datetime_obj = get_new_file_timestamp(filepath)
    #timestamp = time.mktime(new_datetime_obj.timetuple())
    timestamp = datetime.timestamp(new_datetime_obj)
    os.utime(filepath, (timestamp, timestamp))

    file_stat_after = os.stat(filepath)
    
    if(not isVerbose):
        print("{0}: {1} -> {2}"
              # .format(get_filename(filepath),
              .format(filepath,
                      str(datetime.fromtimestamp(file_stat_before.st_mtime)),
                      str(datetime.fromtimestamp(file_stat_after.st_mtime))) )
    else:
        print("""file timestamp, before: \n creation time = {0}\n modified time = {1}\n access time = {2}
                \nfile timestamp, after: \n creation time = {3}\n modified time = {4}\n access time = {5}"""
              .format(str(datetime.fromtimestamp(file_stat_before.st_ctime)),
                      str(datetime.fromtimestamp(file_stat_before.st_mtime)),
                      str(datetime.fromtimestamp(file_stat_before.st_atime)),
                      str(datetime.fromtimestamp(file_stat_after.st_ctime)),
                      str(datetime.fromtimestamp(file_stat_after.st_mtime)),
                      str(datetime.fromtimestamp(file_stat_after.st_atime)))
              )
    

""" Get video clip duration and add it to parsed timestamp """
def get_new_file_timestamp(filepath):
    clip_duration_sec = get_clip_duration_sec(filepath)
    datetime_obj = parse_datetime(filepath)
    new_datetime_obj = datetime_obj + timedelta(seconds=clip_duration_sec)
    if(isVerbose):
        print("new_datetime_obj = parsed datetime_obj + duration_sec = {0} + {1} = {2}"
              .format(str(datetime_obj), str(clip_duration_sec), str(new_datetime_obj)) )
    return new_datetime_obj


""" Parse timestamp from filename """
def parse_datetime(filepath):
    filename = get_filename(filepath)
    datetime_str = filename[0:15]
    datetime_obj = datetime.strptime(datetime_str, "%Y%m%d_%H%M%S")
    return datetime_obj


def get_filename(path_str):
    #head,tail = ntpath.split(path_str)
    #return tail or ntpath.basename(path_str)
    #return os.path.basename(path_str)
    path = Path(path_str)
    #return path.stem
    return path.name
          
    
def get_clip_duration_sec(filepath):
    clip = VideoFileClip(filepath)
    duration_sec = int(round(clip.duration))
    clip.close
    return duration_sec
    
    
    

if __name__== "__main__" :
    sys.exit(main(sys.argv[1:]))
