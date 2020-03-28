import glob
import cv2
from tqdm import tqdm
from .frametoascii import *


def getFrame(sec, file="NONE", frames=0, cols=80, toddmode="n"):
    if file == "NONE":
        return False
    cap = cv2.VideoCapture(file)
    cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = cap.read()
    if hasFrames:
        cv2.imwrite("cache/z_" + file + "_ext_" + str(frames) + ".jpg", image)
        frameAscii("cache/z_" + file + "_ext_" + str(frames) + ".jpg", prog=frames, col=cols,
                   ToddMode=toddmode)
    return hasFrames


def extract(file="NONE", fps=0.099, cols=80, toddmode="n"):
    current_dir = os.getcwd()
    print("INFO: Current dir is " + current_dir)
    print("INFO: Target FPS is " + str(fps))
    try:
        print("INFO: Extraction coming up... This could take a while, go grab a coffee!")
        sec = 0
        frameRate = fps
        success = getFrame(sec, file, frames=0, cols=cols, toddmode=toddmode)
        cap = cv2.VideoCapture(file)
        cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        property_id = int(cv2.CAP_PROP_FRAME_COUNT)
        for i in tqdm(range(int(cv2.VideoCapture.get(cap, property_id))), unit="pics"):
            sec = sec + frameRate
            sec = round(sec, 2)
            success = getFrame(sec, file, i, cols, toddmode=toddmode)
        files = glob.glob("cache/z_" + file + "_ext_*")
        print("INFO: Extraction complete, converted " + str(len(files)) + " frames to ASCII art!")
        cv2.destroyAllWindows()
        return len(files)
    except FileNotFoundError:
        print("ERROR: CV2 failed to extract frames or something went wrong during conversion. Check cache folder for "
              "latest frame and if an error is displayed submit it using a GitHub issue! Probably caused by an "
              "invalid path/non existing path!")
        return 1


def cleanup(file="NONE"):
    for fname in tqdm(os.listdir("cache/")):
        if fname.startswith("z_" + file + "_ext_"):
            os.remove(os.path.join("cache/" + fname))
        if fname.startswith("out_"):
            os.remove(os.path.join("cache/" + fname))
