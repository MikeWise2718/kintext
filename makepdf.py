import argparse
import time
import os

import PIL.Image
import glob
from palut import r1, c1, c2, c3, c4, c5, rst

def get_args():
    parser = argparse.ArgumentParser(description="Build Robot ",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # General Settings
    parser.add_argument("-v", "--verbosity", action='store', type=int, default=2,
                        help="0=Errors, 1=Quiet, 2=Normal, 3=Info, 4=Debug")
    parser.add_argument("-a", "--action", action='store',
                        required=False, help="action - b=build, r=rename", default="b")

    # Input Directory
    parser.add_argument("-id", "--inDir", action='store',
                        required=False, help="Input Directory", default="yw1")
    parser.add_argument("-sd", "--sortDir", action='store',
                        required=False, help="Sort Directory Entries", default=False)

    # Output Files
    parser.add_argument("-of", "--outFile", action='store',
                        required=False, help="Output File", default="default")

    # Animation Settings

    args = parser.parse_args()
    return args


def rename(basename, file_jpgList):
    nf = len(file_jpgList)
    _, basefname = os.path.split(basename)
    for inum, f in enumerate(file_jpgList):
        path, _ = os.path.split(f)
        newname = f"{path}/{basefname}_{inum:03d}.jpg"
        print(f"Renaming {f} to {newname}")
        os.rename(f, newname)
    print(f"Renamed {nf} images")


def build_pdf(pdfname, file_jpgList):
    jpgList = []
    for f in file_jpgList:
        jjpg = PIL.Image.open(f).convert("RGB")
        jpgList.append(jjpg)

    jpgList[0].save(pdfname, save_all=True, append_images=jpgList[1:])
    nf = len(jpgList)
    print(f"Saved {nf} images to {pdfname}")


def main():
    startTime = time.time()

    args = get_args()

    print("args")
    print("     verbosity: ", args.verbosity)
    print("     action: ", args.action)
    print("     inDir: ", args.inDir)
    print("     sortDir: ", args.sortDir)
    print("     outFile: ", args.outFile)

    sourcedir = args.inDir
    path, fname = os.path.split(sourcedir)
    pdfname = f"pdf/{fname}.pdf"

    if args.outFile != "default":
        pdfname = args.outFile

    globmask = f"{sourcedir}/*.jpg"
    file_jpgList = glob.glob(globmask)
    if args.sortDir:
        file_jpgList.sort()

    action = args.action
    if action == "r":
        action = "rename"
    elif action == "b":
        action = "build"

    match action:
        case "rename":
            rename(sourcedir, file_jpgList)
        case "build":
            build_pdf(pdfname, file_jpgList)

    elapTime = time.time() - startTime
    print(f"{c1}Execution took {c2}{elapTime:.3f}{rst} secs ")


if __name__ == "__main__":
    main()
