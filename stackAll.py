# from stack import *

import os
from psdtags import *
from tifffile import imwrite
from imagecodecs import imread
import tkinter as tk
from tkinter import filedialog

def stackImages(sourceDir, saveName):
    fileNames = []
    fullFileNames = os.listdir(sourceDir)
    fileNames = []
    for fileName in fullFileNames:
        fileNames.append(os.path.join(sourceDir, fileName))
    layers = []

    # M T A C S - 1 2 3
    sortPrio = {'M':0,
                'T':1,
                'A':2,
                'C':3,
                'S':4}

    class Layer():
        def __init__(self, name, psdLayer, stain, channel):
            self.name = name
            self.psdLayer = psdLayer
            self.stain = stain
            self.channel = channel


    unsortedLayers = []

    for file in fileNames:
        background = imread(file)
        name = os.path.basename(file)
        sInd = name.find('_s')
        stain = name[sInd-1]
        channel = name[sInd + 4]

        layer = PsdLayer(
                    name=name,
                    rectangle=PsdRectangle(0, 0, *background.shape[:2]),
                    channels=[
                        PsdChannel(
                            channelid=PsdChannelId.CHANNEL0,
                            compression=PsdCompressionType.RLE,
                            data=background[..., 0],
                        ),
                        PsdChannel(
                            channelid=PsdChannelId.CHANNEL1,
                            compression=PsdCompressionType.RLE,
                            data=background[..., 1],
                        ),
                        PsdChannel(
                            channelid=PsdChannelId.CHANNEL2,
                            compression=PsdCompressionType.RLE,
                            data=background[..., 2],
                        ),
                    ],
                    mask=PsdLayerMask(),
                    opacity=255,
                    blendmode=PsdBlendMode.SCREEN,
                    blending_ranges=(),
                    clipping=PsdClippingType.BASE,
                    flags=PsdLayerFlag.PHOTOSHOP5
                    | PsdLayerFlag.TRANSPARENCY_PROTECTED,
                    info=[
                        PsdString(PsdKey.UNICODE_LAYER_NAME, name),
                    ],
                )
        newLayer = Layer(name, layer, stain, channel)
        unsortedLayers.append(newLayer)
        
    # custom sort
    layers = sorted(unsortedLayers, key=lambda x: (sortPrio[x.stain] * 3) + int(x.channel))
    layerList = []
    for layer in layers:
        # print(layer.stain, layer.channel)
        layerList.append(layer.psdLayer)


    image_source_data = TiffImageSourceData(
        name='Layered TIFF Test',
        psdformat=PsdFormat.LE32BIT,
        layers=PsdLayers(
            key=PsdKey.LAYER,
            has_transparency=False,
            layers= layerList,
        ),
        usermask=PsdUserMask(
            colorspace=PsdColorSpaceType.RGB,
            components=(65535, 0, 0, 0),
            opacity=50,
        ),
        info=[
            PsdEmpty(PsdKey.PATTERNS),
            PsdFilterMask(
                colorspace=PsdColorSpaceType.RGB,
                components=(65535, 0, 0, 0),
                opacity=50,
            ),
        ],
    )

    imwrite(
        saveName,
        background,
        photometric='rgb',
        metadata=None,
        extratags=[image_source_data.tifftag()],
    )

cwd = os.getcwd()
root = tk.Tk()
root.withdraw()

baseDir = filedialog.askdirectory(initialdir=os.getcwd(), title='Select Folder')

dirNames = os.listdir(baseDir)
saveDir = os.path.join(baseDir, 'stacks')

if not os.path.exists(saveDir):
    os.mkdir(saveDir)

for dir in dirNames:
    if dir != '.DS_Store' and dir != 'stacks':
        # print(os.path.join(baseDir, dir), os.path.join(saveDir, dir + '.tif'))
        stackImages(os.path.join(baseDir, dir), os.path.join(saveDir, dir + '.tif'))