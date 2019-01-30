#!/usr/bin/env python
#coding=utf-8
'''脚本解决的问题背景：
    A电脑（能联网）写的python脚本，现在要放到B电脑上去执行，遇到的第一个问题是如何搭建一个和A电脑一模一样的环境：解决相关依赖

    使用方法：
    （1） A电脑打开cmd 执行:python SolvePythonDependency.py down
    （2）将SolvePythonDependency.py脚本 和Dependency.zip拷到 B电脑的目录下双击该脚本执行
    注意：该脚本不适用有双环境（py2/py3）的电脑
'''
import os
import zipfile
import shutil
import sys
import subprocess
'''
   1.mode = (yes) :联网情况下的依赖解决 (no) :未联网情况下的依赖解决 (down):已有环境包的复制
'''

class SolvePythonDependency:
    #解决windows下python包的依赖问题
    isPrepare = True

    def PrepareCheck(self):
        '当前文件下是否存在依赖包 Dependency.zip和依赖文件Requirement.txt'
        info = "|".join(os.listdir("./"))
        print info
        if "Dependency.zip" not in info:
            print "can`t find file:", "Dependency.zip"
            self.isPrepare = False
            return
        z = zipfile.ZipFile("Dependency.zip")
        z.extractall()
        z.close()


    def AfterDetail(self):
        if os.path.exists("Dependency"):
            shutil.rmtree("Dependency")
        if os.path.exists("Requirements.txt"):
            os.remove("Requirements.txt")
        print "anykey to exit"


    def PrepareDownload(self):
        "准备依赖文件和依赖的包"
        os.system("pip freeze >Requirements.txt")
        targetFile = "Dependency"
        if os.path.exists("./%s"% targetFile):
            shutil.rmtree(targetFile)
        os.mkdir(targetFile)
        child = subprocess.Popen("pip install --download ./%s -r Requirements.txt " % targetFile)
        child.wait()

        # makezip

        z = zipfile.ZipFile("%s.zip" % targetFile,'w')
        z.write("./Requirements.txt")
        for root, subfolders, subfileLists in os.walk(r'./Dependency'):


            #filesname是一个列表，我们需要里面的每个文件名和当前路径组合
                for file in subfileLists:

                    # 将当前路径与当前路径下的文件名组合，就是当前文件的绝对路径
                    z.write(os.path.join(root, file))
        z.close()

    def ConnectI(self):
        "联网情况下"
        os.system("pip install -r Requirements.txt")

    def NoConnectI(self):
        "不联网情况"
        os.system("pip install --no-index --find-links=Dependency -r Requirements.txt")

    def install_with_Net(self):
        "联网情况"
        self.PrepareCheck()
        if self.isPrepare:
            self.ConnectI()
        self.AfterDetail()

    def install_without_Net(self):
        "断网情况下"
        self.PrepareCheck()
        if self.isPrepare:
            self.NoConnectI()
        self.AfterDetail()

def main():
    if len(sys.argv) == 1:
        mode = "no"
    else:
        mode = sys.argv[1]

    solvePythonDependency = SolvePythonDependency()
    if mode == "yes":
        print "install with internet"
        solvePythonDependency.install_with_Net()
    elif mode=="no":
        print "install without internet"
        solvePythonDependency.install_without_Net()

    elif mode =="down":
        print 'create \'Denpendency.zip\''
        solvePythonDependency.PrepareDownload()
        solvePythonDependency.AfterDetail()
    else:
        print 'parameter error ,it is not in [yes,no,down],please enter again!'

if  __name__ == '__main__':
    try:
        main()
    except BaseException,e:
        print e.message
        raw_input()
    raw_input()