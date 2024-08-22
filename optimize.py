import sys
import os
from PIL import Image


cwd = os.getcwd()
dir = os.path.join(cwd, 'test')
Image.MAX_IMAGE_PIXELS = 200000000



for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    if filename.find('.jpg')!= -1:
        im = Image.open(f)
        # print('im format:', im.format, 'dpi', im.info['dpi'])
        width, height = im.size
        im1 = im
        # print('im1 format:', im.format, im.info['dpi'])
        im1.save(f, format = 'JPEG', dpi = im1.info['dpi'])#, quality = 'keep')