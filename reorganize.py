import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog


cwd = os.getcwd()
root = tk.Tk()
root.withdraw()

sourceDir = filedialog.askdirectory(initialdir=os.getcwd(), title='Select Folder')
newDir = sourceDir + '_reordered'
if os.path.exists(newDir):
    print(newDir + 'already exists')
else:
    os.mkdir(newDir)
    fileList = os.listdir(sourceDir)
    for filename in fileList:
        # print(filename)
        sampleInd = filename.find('_s')
        layerInd = filename.find('_FL')
        if layerInd == -1:
            layerInd = filename.find('_ML')

        if layerInd == -1 and sampleInd == -1:
            continue
        layer = filename[layerInd + 3]
        sample = filename[sampleInd + 2]

        dirname = os.path.join(sourceDir + '_reordered', 'L' + layer + '_s' + sample)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        shutil.copyfile(os.path.join(sourceDir,filename), os.path.join(dirname, filename))