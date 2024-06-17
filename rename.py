import os
import shutil
import re

cwd = os.getcwd()
sourceDir = 'test1'
# destDir = 'new'
dir = os.path.join(cwd, sourceDir)
# print(dir)
fileList = os.listdir(dir)
fileList.sort()


# case: m
for filename in fileList:
    f = os.path.join(dir, filename)
    ind = filename.find('_m')
    if  ind != -1 : #filter for make-up, only one at a time (m#)
        print('filename:', filename)
        makeup = filename[ind + 2]
        sampleInd = filename.find('_s') 
        # print(type(makeup))
        # print(type(filename[sampleInd+2]))
        
        base = filename[:ind]
        
        if sampleInd != -1:  #case: contains s#
            if makeup != filename[sampleInd+2]:
                print('deleting', os.path.join(dir, filename))
                os.remove(os.path.join(dir, filename))
        else: # case: doesnt have s#: add it in
            newname = filename[:ind + 3] + '_s' + makeup + filename[-6:]
            # print(newname)
            print('renaming', filename, 'to', newname)
            os.rename(os.path.join(dir, filename),os.path.join(dir, newname))
            filename = newname
        

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

        newname = base + '_s' + makeup + 'c' + c +'.jpg'
        print('renaming', filename, 'to', newname)
        os.rename(os.path.join(dir, filename),os.path.join(dir, newname))


        # print(makeup)
        # print(base)
        # case: multiple samples
    
    
# case: r
# for filename in fileList:
#     f = os.path.join(dir, filename)
#     ind = filename.find('_r')
#     if  ind != -1:
        
#         print(filename)
