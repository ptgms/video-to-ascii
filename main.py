import argparse
from Tools.bundle import bundle_to_py
from Tools.mp4_lower_fps import *


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
    parser.add_argument('--toddmode', dest='toddmode', required=False, help="OPTIONAL: Makes the generated ASCII mode "
                                                                            "7 times the detail. It probably won't "
                                                                            "look good, so it defaults to n")
    parser.add_argument('--totalframes', dest='totalframes', required=False, help="OPTIONAL: Displays total amount of "
                                                                                  "frames in an Video and then closes"
                                                                                  " the program. Usage is "
                                                                                  "--totalframes y/n.")

    # parse args
    args = parser.parse_args()

    if args.clean:
        if str(args.clean) == "yes" or "y":
            print("INFO: Got cleanup request, cleaning previous trash... This could take a while!")
            cleanup(args.vidFile)
            exit()

    if args.scale:
        cols = 80 * int(args.scale)
    else:
        scale = False

    if args.toddmode:
        if str(args.toddmode) == "yes" or "y":
            todd = "y"
            print("INFO: Todd Mode activated. 7 times the detail.")
        else:
            todd = "n"
    else:
        todd = False

    if args.fps:
        tofps = int(args.fps)
        print("Got option fps to " + str(tofps))
    else:
        tofps = False
    videoFile = args.vidFile

    if args.totalframes:
        if str(args.clean) == "yes" or "y":
            print("INFO:")
            print(gettotalframes(videoFile))
            exit()

    if args.audio:
        if str(args.audio) == "yes" or "y":
            audioext(videoFile)
            audio = True
        else:
            audio = False
    else:
        audio = False

    if os.path.exists("final_out " + videoFile + ".py"):
        print("Already existing output file, removing now.")
        os.remove("final_out " + videoFile + ".py")

    if os.path.exists("cache/out_0.txt"):
        print("Temporary outputs still exist, assuming it's all alright, skipping to bundle...")
        target_frames = len(os.listdir("cache/"))
        bundle_to_py(videoFile, audio, target_frames)
        print("Successfully converted, cleaning up...")
        finished(videoFile)
        exit(0)

    if tofps:
        if args.scale:
            total_frames = extract(videoFile, tofps, toddmode=todd, cols=cols)
        else:
            total_frames = extract(videoFile, tofps, toddmode=todd)
    else:
        if args.scale:
            total_frames = extract(videoFile, toddmode=todd, cols=cols)
        else:
            total_frames = extract(videoFile, toddmode=todd)

    if total_frames != 0:
        print("ERROR: Something has happened during the extraction/conversion. It should be printed out above. "
              "Cleaning up cache now and exiting...")
        finished(videoFile)
        exit(0)

    target_frames = len(os.listdir("cache/"))

    bundle_to_py(videoFile, audio, target_frames)

    print("Successfully converted, cleaning up...")
    finished(videoFile)
    exit(0)


# call main
if __name__ == '__main__':
    main()
