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
    parser.add_argument('--file', dest='vidFile', required=True)
    parser.add_argument('--audio', dest='audio', required=False)
    parser.add_argument('--clean', dest='clean', required=False)

    # parse args
    args = parser.parse_args()

    if args.clean:
        cleanup(args.vidFile)
        exit()


    videoFile = args.vidFile

    if args.audio:
        audioext(videoFile)
        audio = True
    else:
        audio = False

    if os.path.exists("final_out " + videoFile + ".py"):
        print("Already existing output file, removing now.")
        os.remove("final_out " + videoFile + ".py")

    if os.path.exists("out_0.txt"):
        print("Temporary outputs still exist, assuming last attempt unsuccessful, cleaning up...")
        cleanup(videoFile)

    total_frames = extract(videoFile)

    if total_frames == 0:
        print("An error occured while extracting the frames. Cleaning up workspace now...")
        cleanup(videoFile)

    count = 0
    print("Converting frames to ASCII now...")
    for i in tqdm(range(total_frames)):
        frameAscii("z_" + videoFile + "_ext_" + str(i) + ".jpg", prog=count)
        count = count + 1

    bundle_to_py(videoFile, audio, total_frames)

    print("Succesfully converted, cleaning up...")
    finished(videoFile)
    exit(0)


# call main
if __name__ == '__main__':
    main()
