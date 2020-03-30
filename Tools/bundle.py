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
        f2 = open("cache/out_" + str(i) + ".txt", 'r', errors='ignore')
        store = f2.read()
        temp = template2.replace("REPLACE", str(store))
        f.write(temp.replace("RPLC", str(delay)))
        f2.close()

    f.close()
    template.close()


def bundle_to_cpp(file="NONE", audio=False, frames=0):
    delay = getdur(file, frames)
    template = open("templates/top.cpp", "r", encoding="utf8")
    template2 = template.read()
    f = open("final_out_" + file + ".cpp", 'w', encoding="utf8")
    f.write("#include <iostream>\n#include <chrono>\n#include <thread>\n")
    if audio:
        f.write("#include <Windows.h>\n#include <MMSystem.h>\n")
    f.write("\n\nint main() {\n")
    print("Bundling to a CPP file now...")
    if audio:
        f.write("""PlaySound(TEXT("fout_audio.wav"), NULL, SND_ASYNC);\n""")
    for i in tqdm(range(frames)):
        f2 = open("cache/out_" + str(i) + ".txt", 'r', errors='ignore')
        store = f2.read()
        temp = template2.replace("REPLACE", str(store))
        f.write(temp.replace("RPLC", "85"))
        f2.close()
    f.write("}")
    f.close()
    template.close()
    print("!!!WARNING!!! In order for this to work, add Winmm.lib as an Input dependency in Visual Studio.")
