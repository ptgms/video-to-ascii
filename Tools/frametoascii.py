import os
import numpy as np
from PIL import Image

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,^`'. "

gscale2 = '@%#*+=-:. '


def getAverageL(image):
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w * h))


count = 0


def covertImageToAscii(fileName, cols, scale, ToddMode="n"):
    global gscale1, gscale2
    image = Image.open(fileName).convert('L')
    W, H = image.size[0], image.size[1]

    w = W / cols
    h = w / scale

    rows = int(H / h)

    if cols > W or rows > H:
        print("Video too small for specified cols!")
        exit(0)

    aimg = []
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)
        if j == rows - 1:
            y2 = H
        aimg.append("")
        for i in range(cols):
            x1 = int(i * w)
            x2 = int((i + 1) * w)
            if i == cols - 1:
                x2 = W
            img = image.crop((x1, y1, x2, y2))
            avg = int(getAverageL(img))
            if ToddMode == "y":
                gsval = gscale1[int((avg * 67) / 255)]
            else:
                gsval = gscale2[int((avg * 9) / 255)]
            aimg[j] += gsval
    return aimg


def frameAscii(file="NONE", out="None", scaler=0, col=80, fname=str, prog=int, ToddMode="n", outtype="py"):
    if not fname:
        exit("ERROR!")
    outFile = "cache/out_" + str(prog) + ".txt"

    scale = 0.43

    cols = col

    aimg = covertImageToAscii(file, cols, scale, ToddMode)

    f = open(outFile, 'w')
    #print("Info: Out type is " + outtype)
    if outtype == "py":
        for row in aimg:
            f.write("\"" + row + r"\n" + "\"")
    else:
        for row in aimg:
            f.write("\"" + row + r"\n" +"\"\n")

    f.close()
    os.remove(file)


def audioext(file="NONE", out="py"):
    if file == "NONE":
        exit()
    import moviepy.editor as mp
    clip = mp.VideoFileClip(file)
    if out == "py":
        clip.audio.write_audiofile("fout_audio.mp3")
    else:
        clip.audio.write_audiofile("fout_audio.wav")


def getdur(file="NONE", total=0, totalfps=10):
    if file == "NONE" or total == 0:
        exit()
    from moviepy.editor import VideoFileClip
    clip = VideoFileClip(file)
    if totalfps != 10:
        return clip.duration / total
    elif clip.duration <= 10:
        return clip.duration / total
    else:
        return 0.099


def gettotalframes(file="NONE", fps=0.1):
    if file == "NONE":
        exit()
    import cv2
    cap = cv2.VideoCapture(file)
    cap.set(cv2.CAP_PROP_POS_MSEC, 0 * 1000)
    property_id = int(cv2.CAP_PROP_FRAME_COUNT)
    length = int(cv2.VideoCapture.get(cap, property_id))
    return length
