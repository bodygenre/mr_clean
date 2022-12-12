#! /usr/bin/env python3

import argparse
from ast import AsyncFunctionDef
import random
import magic
import sys
import os

default_percentage = 100.0
# default_cleanup_paths = ["/home/hd1/tetsuharu/media", "/home/hd1/tetsuharu/torrents/data"]
default_cleanup_paths = ["/home/user/Videos"]
default_output_path = sys.stdout
sort_choices = ["size_dec", "size_acc", "alpha_dec", "alpha_acc", "date_dec", "date_acc"]

def get_video_files(path_list):    
    #counter = 0
    videos = []
    #print("Cleanpaths: {}".format(args.cleanpaths))
    for path in path_list:
        #print("Finding files in {}".format(path))
        for (root,dirs,files) in os.walk(os.path.abspath(path)):
            #print("{}\t{}\t{}".format(root, dirs, files)) # Lots of output
            for file in files:
                fullpath = os.path.join(root, file)
                #if "video" in magic.from_file(fullpath, mime=True):
                #print(magic.from_file(fullpath, mime=True))
                if "video" in magic.from_file(fullpath, mime=True):
                    #counter += 1
                    #print("{} VIDYA".format(counter))
                    videos.append(fullpath)
    return videos

def decimate_list(percent, list_to_decimate):    
    print(percent)
    if (percent == 0):
        return []
    for _ in range(int(len(list_to_decimate) * (percent / 100.0))):
        #print(random.randrange(0, len(list_to_decimate)))
        list_to_decimate.pop(random.randrange(0, len(list_to_decimate)))    
    
    return list_to_decimate

def sort_list(sort, list_to_sort):
    return list_to_sort

def main():
    parser=argparse.ArgumentParser(description="A muscular bald man who frees up disk space.")

    # defining arguments for parser object
    parser.add_argument("-%", "--percent", type = float, nargs = 1,
                        metavar = "num", default = default_percentage, choices=range(0,100),
                        help = "Percentage of the files in the cleanup paths to print in output. Defaults to " + default_percentage.__str__())
    
    parser.add_argument("-o", "--output", type = str, nargs = 1,
                        metavar = "output", default = default_output_path,
                        help = "Path to an output file. Defaults to " + str(default_output_path) + ".")

    parser.add_argument("-c", "--cleanpaths", type = str, nargs = '*',
                        metavar = ("path1", "path2"), default = default_cleanup_paths,
                        help = "Space-separated paths to include in cleanup operations. Defaults to \"" + " ".join(default_cleanup_paths) + "\".")

    parser.add_argument("-s", "--sortby", type = str, nargs = 1,
                        metavar = 'option', default = "size_dec", choices = sort_choices,
                        help = "How to sort the output. Choices are " + ", ".join(sort_choices) + ".")


    # parse the arguments from standard input
    args = parser.parse_args()

    vid_list = get_video_files(args.cleanpaths)
    vid_list = decimate_list(args.percent[0], vid_list)
    vid_list = sort_list(args.sortyby[0], vid_list)

    print(vid_list)
    print(len(vid_list))

if __name__ == "__main__":
    # calling the main function
    main()



'''
print("finding files in media/")
mFiles = []
for (root,dirs,files) in os.walk(os.path.abspath(mediaPath)):
    for file in files:
        real_path = os.path.realpath(os.path.join(root, file))
        path_test = os.path.islink(os.path.join(root, file))
        if path_test is True:
             mFiles.append(real_path) 

print("finding files in torrents/data/")
for (root,dirs,files) in os.walk(os.path.abspath(tdPath)):
    for file in files:
        tdFile = os.path.join(root, file)
        if tdFile not in mFiles:
             print(tdFile)
'''

'''
import os

mediaPath = "/home/hd1/tetsuharu/media"
tdPath = "/home/hd1/tetsuharu/torrents/data"
tdPath2 = "/home/hd1/tetsuharu/torrents/completed"

def getTorrentFiles():    
    tdfiles = set()
    for path in [ tdPath, tdPath2 ]:
        print("finding files in {path}")
        for (root,dirs,files) in os.walk(os.path.abspath(tdPath)):
            for file in files:
                tdFile = os.path.join(root, file)
                tdfiles.add(tdFile)
    return tdfiles


def getMediaTorrentFiles():
    print("finding files in media/")
    mFiles = set()
    for (root,dirs,files) in os.walk(os.path.abspath(mediaPath)):
        for file in files:
            real_path = os.path.realpath(os.path.join(root, file))
            path_test = os.path.islink(os.path.join(root, file))
            if path_test is True:
                mFiles.add(real_path)
    return mFiles

'''

# Find files in the plex media directories
# Identify symlinks
# Determine if there are symlinks without  in the 
# Find files in the torrents directories
# Cr