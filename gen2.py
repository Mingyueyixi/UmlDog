# coding=utf-8
# @author rongtao lu
# python2脚本，window下双击运行。

import os
import re
import chardet


class FileUtils():

    def __init__(self):
        self.allpaths = []

    def getallfile(self, path, mregex):
        currfiles = os.listdir(path)
        for file in currfiles:
            filepath = os.path.join(path, file)
            if os.path.isdir(filepath):
                self.getallfile(filepath, mregex)
            elif os.path.isfile(filepath) and re.match(mregex, filepath):
                self.allpaths.append(filepath)
        return self.allpaths


def deepUnifyScale(mregex):
    if not umlscale:
        return
    print("统一自动缩放比例：{}".format(umlscale))
    allfiles = FileUtils().getallfile("./", mregex)
    for fpath in allfiles:
        unifyScale(fpath)


def unifyScale(path):
    if not umlscale:
        return
    file = open(path, "rb+")
    filebin = file.read()

    coderesult = chardet.detect(filebin)
    if not coderesult["encoding"]:
        coderesult["encoding"] = "utf-8"
    content = filebin.decode(encoding=coderesult["encoding"])

    if re.search(r'\n\s*scale\s*\d*[.]?\d*;?', content, re.I):
        content = re.sub(r'\n\s*scale\s*\d*[.]?\d*;?', "\nscale {}".format(umlscale), content, 1, re.I)
        print(path)
    elif re.search(r"^\s*@startuml\s*", content, re.I):
        content = re.sub(r"^\s*@startuml\s*", "@startuml\nscale {}\n".format(umlscale),content,1,re.I)
        print(path)
    else:
        print("skip：{}".format(path))
    file.seek(0, 0)
    file.truncate()
    file.write(bytes(content,coderesult["encoding"]))
    file.flush()
    file.close()


def genBuild(mregex):
    options = ["-svg", "-png"]
    baseCmd = 'java -Dfile.encoding=utf-8 -jar "plantuml.jar" "{}" "{}"'
    cmmods = []
    for option in options:
        cmmods.append(baseCmd.format(mregex, option))

    cmd = " && ".join(cmmods)
    print(cmd)

    cmdf = os.popen(cmd, "r")
    output = cmdf.read()
    cmdf.close()

    print(output)


umlscale = 1.5

if __name__ == '__main__':
    deepUnifyScale(r".*\.puml")
    genBuild("**/*.puml")
    print(re.search(r"^\s*@startuml\s*", "@startuml\nstart", re.I))
