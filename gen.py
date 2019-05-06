# coding=utf-8
import os
import re

umlscale = 1.2


def copyTo(src, dir):
    # py3默认系统编码读取。即gbk
    srcf = open(src, "r",encoding="utf-8")
    dirpath = dir + "/" + os.path.basename(srcf.name)
    srcbin = srcf.read()

    if umlscale:
        print("set scale：" + str(umlscale))
        if re.search(r"\n[ 	]*scale[ 	]*[\d;.]*", srcbin, re.M | re.I):
            srcbin = re.sub(r"\n[ 	]*scale[ 	]*[\d;.]*", "\nscale " + str(umlscale), srcbin, 1,re.M|re.I)
        else:
            srcbin = srcbin.replace("@startuml", "@startuml\nscale {}".format(str(umlscale)))
    srcf.flush()
    srcf.close()
    if not srcbin: return

    dirf = open(dirpath, "w+")
    dirf.write(srcbin)
    dirf.flush()
    dirf.close()


def getPumlPath(dir):
    files = os.listdir(dir)
    pumls = []
    for f in files:
        if (f.endswith(".puml")):
            pumls.append(dir + "/" + f)
    return pumls


def prepare():
    if not os.path.exists("src"): return
    if not os.path.exists("build"):
        os.mkdir("build")
    if not os.path.exists("dist/png"):
        os.makedirs("dist/png")
    if not os.path.exists("dist/svg"):
        os.makedirs("dist/svg")
    pumls = getPumlPath("src")
    for p in pumls:
        copyTo(p, "build")


def genBuild():
    prepare()
    pumls = getPumlPath("build")
    # batTemp = open("build/gen.bat")
    print(pumls)
    cmd = ""
    baseCmd = 'java -Dfile.encoding=utf-8 -jar "plantuml.jar" {} "{}" && '
    cpCmd = 'copy /y "{}" "dist\\{}" && '
    for uf in pumls:
        end = uf.rindex(".")
        ufname = uf[0:end].replace("/", "\\")

        cmd += baseCmd.format("-tsvg", uf)
        cmd += cpCmd.format(ufname + ".svg", "svg")

        cmd += baseCmd.format("-t", uf)
        cmd += cpCmd.format(ufname + ".png", "png")

    cmd = cmd[0:-4]
    print(cmd)
    print(os.popen(cmd).read())

if __name__ == '__main__':
    genBuild()
