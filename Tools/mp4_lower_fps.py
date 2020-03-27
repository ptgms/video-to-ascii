import cv2
import os
import glob
from tqdm import tqdm
import glob


def getFrame(sec, file="NONE", frames=0):
    if file == "NONE":
        return False
    cap = cv2.VideoCapture(file)
    cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
    hasFrames, image = cap.read()
    if hasFrames:
        cv2.imwrite("cache/z_" + file + "_ext_" + str(frames) + ".jpg", image)
    return hasFrames


def extract(file="NONE", fps=0.1):
    current_dir = os.getcwd()
    print("INFO: Current dir is " + current_dir)
    print("INFO: Target FPS is " + str(fps))
    try:
        print("INFO: Extraction coming up... This could take a while, go grab a coffee!")
        sec = 0
        frameRate = fps
        frames = 0
        success = getFrame(sec, file)
        while success:
            sec = sec + frameRate
            sec = round(sec, 2)
            success = getFrame(sec, file, frames)
            frames = frames + 1
        files = glob.glob("cache/z_" + file + "_ext_*")
        print("INFO: Extraction complete, got " + str(len(files)) + " frames to convert!")
        cv2.destroyAllWindows()
        return len(files)
    except FileNotFoundError:
        print("ERROR: CV2 failed to extract frames! Probably caused by an invalid path/non existing path!")
        return 0


def cleanup(file="NONE"):
    for fname in tqdm(os.listdir("cache/")):
        if fname.startswith("z_" + file + "_ext_"):
            os.remove(os.path.join("cache/" + fname))
        if fname.startswith("out_"):
            os.remove(os.path.join("cache/" + fname))
