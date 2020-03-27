import os
import sys, random, argparse
import numpy as np
import math

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

gscale2 = '@%#*+=-:. '


def getAverageL(image):
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w * h))


from PIL import Image

count = 0


def covertImageToAscii(fileName, cols, scale):
    global gscale1, gscale2
    image = Image.open(fileName).convert('L')
    W, H = image.size[0], image.size[1]

    w = W / cols
    h = w / scale

    rows = int(H / h)

    if cols > W or rows > H:
        print("Image too small for specified cols!")
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
            gsval = gscale2[int((avg * 9) / 255)]
            aimg[j] += gsval
    return aimg


def frameAscii(file="NONE", out="None", scale=0, col=0, fname=str, prog=int):
    if not fname:
        exit("ERROR!")
    outFile = "cache/out_" + str(prog) + ".txt"

    scale = 0.43
    if scale != 0:
        scale = float(scale)

    cols = 80
    if col != 0:
        cols = int(cols)

    aimg = covertImageToAscii(file, cols, scale)

    f = open(outFile, 'w')

    for row in aimg:
        f.write(row + "\n")

    f.close()


def audioext(file="NONE"):
    if file == "NONE":
        exit()
    import moviepy.editor as mp
    clip = mp.VideoFileClip(file)
    clip.audio.write_audiofile("fout_audio.mp3")


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


def gettotalframes(file="NONE"):
    if file == "NONE":
        exit()
    import cv2
    cap = cv2.VideoCapture(file)
    property_id = int(cv2.CAP_PROP_FRAME_COUNT)
    length = int(cv2.VideoCapture.get(cap, property_id))
    return length
