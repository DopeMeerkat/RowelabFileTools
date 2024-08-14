import os
import sys
import shutil
import tkinter as tk
from tkinter import filedialog


cwd = os.getcwd()
root = tk.Tk()
root.withdraw()

sourceDir = filedialog.askdirectory(initialdir=os.getcwd(), title='Select Folder')
newDir = sourceDir + '_renamed'
if os.path.exists(newDir):
    print(newDir + 'already exists')
else:
    # os.mkdir(newDir)

    shutil.copytree(sourceDir, newDir)
    dir = os.path.join(cwd, newDir)
    # dir = os.path.join(cwd, sourceDir)
    fileList = os.listdir(dir)
    fileList.sort()

    # separate makeups into individuals
    for filename in fileList:
        ind = filename.find('_m')
        sInd = filename.find('_s')
        if  ind != -1 and sInd != -1:
            # print('filename =', filename)
            base = filename[:ind]
            makeup = filename[ind+2:sInd]
            newName = base + '_m' + makeup[int(filename[sInd + 2])-1] + '_' + filename[-6:]
            # print('newname =', newName)
            print('renaming', filename, 'to', newName)
            os.rename(os.path.join(dir, filename),os.path.join(dir, newName))

    fileList = os.listdir(dir) #update list
    fileList.sort()
                
    # case: m
    for filename in fileList:
        ind = filename.find('_m')
        if  ind != -1 : #filter for make-up, only one at a time (m#)
            makeup = filename[ind + 2]
            sampleInd = filename.find('_s') 
            if sampleInd != -1:  #case: contains s#
                if makeup != filename[sampleInd+2]:
                    print('deleting', os.path.join(dir, filename))
                    os.remove(os.path.join(dir, filename))
            else: # case: doesnt have s#: add it in
                newFilename = filename[:ind + 3] + '_s' + makeup + filename[-6:]
                # print(newFilename)
                print('renaming', filename, 'to', newFilename)
                os.rename(os.path.join(dir, filename),os.path.join(dir, newFilename))
                filename = newFilename


    fileList = os.listdir(dir) #update list
    fileList.sort()
    for filename in fileList:
        ind = filename.find('_m')
        if  ind != -1 : #filter for make-up, only one at a time (m#)
            makeup = filename[ind + 2]
            sampleInd = filename.find('_s') 
            
            base = filename[:ind]
            
            c = filename[-5]
            # print('c', c)
            fileList = os.listdir(dir) #update list
            fileList.sort()
            for file in reversed(fileList):
                if file.find(base) != -1 and file.find('m') == -1 and file[-5] == c:
                    sInd = file.find('_s')+2
                    if  file[sInd] >= makeup:
                        newname = base + '_s' + str(int(file[sInd])+1) + 'c' + str(c) + '.jpg'
                        print('renaming', file, 'to', newname)
                        os.rename(os.path.join(dir, file),os.path.join(dir, newname))
            

            if makeup == filename[-7]: # 
                newname = base + filename[-9:] #remove _m#
                print('-renaming', filename, 'to', newname)
                os.rename(os.path.join(dir, filename),os.path.join(dir, newname))

        
    # case: r
    for filename in fileList:
        ind = filename.find('_r')
        if  ind != -1:
            # print('filename:', filename)
            base = filename[:ind]
            
            if filename[ind:-9].find(filename[-7]):
                # print(filename[ind])
                basefile = base + filename[-9:]
                print('replacing', basefile, 'with', filename)
                os.replace(os.path.join(dir, filename),os.path.join(dir, basefile))