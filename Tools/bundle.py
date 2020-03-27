import os
from tqdm import tqdm
from .frametoascii import getdur


def bundle_to_py(file="NONE", audio=False, frames=0):
    delay = getdur(file, frames)
    template = open("templates/top.py", "r", encoding="utf8")
    template2 = template.read()
    f = open("final_out " + file + ".py", 'w', encoding="utf8")
    f.write("import os\nfrom time import sleep\n\n")
    if audio:
        f.write("""import playsound\nplaysound.playsound('fout_audio.mp3', False)\n""")
    print("Bundling to a python file now...")
    for i in tqdm(range(frames)):
        print(str(i) + "/" + str(frames))
        f2 = open("cache/out_" + str(i) + ".txt", 'r', errors='ignore')
        store = f2.read()
        temp = template2.replace("REPLACE", str(store))
        f.write(temp.replace("RPLC", str(delay)))
        f2.close()

    f.close()
    template.close()
