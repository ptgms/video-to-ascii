import sys, random, argparse
import numpy as np
import math
from tqdm import tqdm
from Tools.bundle import bundle_to_py
from Tools.frametoascii import *
from PIL import Image
from Tools.mp4_lower_fps import *

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

gscale2 = '@%#*+=-:. '


def finished(file="NONE"):
    cleanup(file)


# main() function
def main():
    # create parser
    descStr = "This program converts an video into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='vidFile', required=True, help="The path to the Video file. If in current "
                                                                      "directory, typing in the file name is fine.")
    parser.add_argument('--audio', dest='audio', required=False, help="OPTIONAL: Argument whether or not to include "
                                                                      "audio in the final product. Usage is --audio "
                                                                      "y/n or exclude it completely.")
    parser.add_argument('--fps', dest='fps', required=False, help="OPTIONAL: Target ms delay for the final product. "
                                                                  "Default is 0.1ms. Usage is --fps int or exclude it "
                                                                  "completely.")
    parser.add_argument('--scale', dest='scale', required=False, help="OPTIONAL: Scale factor of the final product. "
                                                                      "Usage is --scale int")
    parser.add_argument('--clean', dest='clean', required=False, help="OPTIONAL: Argument to clean previous program "
                                                                      "cache in case of failure. Usage is --clean y/n")
    parser.add_argument('--totalframes', dest='totalframes', required=False, help="OPTIONAL: Displays total amount of "
                                                                                  "frames in an Video and then closes"
                                                                                  " the program. Usage is "
                                                                                  "--totalframes y/n.")

    # parse args
    args = parser.parse_args()

    if args.clean:
        print("INFO: Got cleanup request, cleaning previous trash... This could take a while!")
        cleanup(args.vidFile)
        exit()

    if args.scale:
        scale = int(args.scale)

    if args.fps:
        tofps = int(args.fps)
        print("Got option fps to " + str(tofps))
    else:
        tofps = False
    videoFile = args.vidFile

    if args.totalframes:
        print("INFO:")
        print(gettotalframes(videoFile))
        exit()

    if args.audio:
        audioext(videoFile)
        audio = True
    else:
        audio = False

    if os.path.exists("final_out " + videoFile + ".py"):
        print("Already existing output file, removing now.")
        os.remove("final_out " + videoFile + ".py")

    if os.path.exists("cache/out_0.txt"):
        print("Temporary outputs still exist, assuming last attempt unsuccessful, cleaning up...")
        cleanup(videoFile)

    if tofps:
        total_frames = extract(videoFile, tofps)
    else:
        total_frames = extract(videoFile)
    if total_frames == 0:
        print("An error occured while extracting the frames. Cleaning up workspace now...")
        cleanup(videoFile)

    count = 0
    print("Converting frames to ASCII now...")
    for i in tqdm(range(total_frames)):
        if args.scale:
            frameAscii("cache/z_" + videoFile + "_ext_" + str(i) + ".jpg", prog=count, scale=scale)
        else:
            frameAscii("cache/z_" + videoFile + "_ext_" + str(i) + ".jpg", prog=count)
        count = count + 1

    bundle_to_py(videoFile, audio, total_frames)

    print("Successfully converted, cleaning up...")
    finished(videoFile)
    exit(0)


# call main
if __name__ == '__main__':
    main()
