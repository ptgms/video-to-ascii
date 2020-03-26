import cv2
import os
import glob

def extract(file="NONE"):
    dir = os.getcwd()
    print("INFO: Current dir is " + dir)
    try:
        print("INFO: Extraction coming up...")
        cap = cv2.VideoCapture(file)
        cap.set(cv2.CAP_PROP_FPS, 10)
        i = 0
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            cv2.imwrite('z_' + file + '_ext_' + str(i) + '.jpg', frame)
            i += 1
        print("INFO: Extraction complete, got " + str(i) + " frames to convert!")
        cap.release()
        cv2.destroyAllWindows()
        return i
    except FileNotFoundError:
        print("ERROR: CV2 failed to extract frames! Probably caused by an invalid path/non existing path!")
        return 0


def cleanup(file="NONE"):
    for fname in os.listdir("."):
        if fname.startswith("z_" + file + "_ext_"):
            os.remove(os.path.join(fname))
        if fname.startswith("out_"):
            os.remove(os.path.join(fname))

