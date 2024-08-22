import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image

# TODO: 
# - loaded image != viewing image
# - path before directory contains '_type'
# - iterate backwards
# - left and right
# - resolution decreased?

Image.MAX_IMAGE_PIXELS = 200000000
IMAGE_HEIGHT = 1100 # minimum height of image in pixels, change if needed based on device
IMAGE_WIDTH = 800  # minimum width of image in pixels
cropSpd = 4 # crop speed

types = ['A', 'M', 'T', 'S'] # list of different types of images
viewingImage = {'A': '2', 'M': '1', 'T': '1', 'S': '0'} # channel that is most visible, 0 indicates only 1 channel
channelAmount = {'A': 3, 'M': 4, 'T': 3, 'S': 1} # total number of different channels 

class GraphicView(QtWidgets.QGraphicsView):
    rectChanged = QtCore.pyqtSignal(QtCore.QRect)

    def __init__(self, *args, **kwargs):
        QtWidgets.QGraphicsView.__init__(self, *args, **kwargs)
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.setMouseTracking(True)
        self.origin = QtCore.QPoint()
        self.changeRubberBand = False

        self.scene = QtWidgets.QGraphicsScene()
        
        self.setScene(self.scene)
        self.selectedRegion = {'x':0,'y':0,'w':-1,'h':-1}
        self.graphicsPixmapItem = None


    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
        self.rectChanged.emit(self.rubberBand.geometry())
        self.rubberBand.show()
        self.changeRubberBand = True
        QtWidgets.QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.changeRubberBand:
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())
            self.rectChanged.emit(self.rubberBand.geometry())
        QtWidgets.QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.changeRubberBand = False
        QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)
        self.selectedRegion['x'] = self.rubberBand.geometry().x()
        self.selectedRegion['y'] = self.rubberBand.geometry().y()
        self.selectedRegion['w'] = self.rubberBand.geometry().width()
        self.selectedRegion['h'] = self.rubberBand.geometry().height()
        self.scene.addRect(self.selectedRegion['x'],self.selectedRegion['y'],self.selectedRegion['w'],self.selectedRegion['h'], pen = QtGui.QPen(QtCore.Qt.red, 4))
        self.rubberBand.hide()

class ImageLoader(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QGridLayout(self)

        self.label = GraphicView()
        layout.addWidget(self.label, 1, 2, 1, 2)
        self.label.setMinimumSize(IMAGE_WIDTH, IMAGE_HEIGHT)
        self.label.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.label.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # the label alignment property is always maintained even when the contents
        # change, so there is no need to set it each time
        self.setWindowTitle('Cropping Tool')

        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.loadImageButton = QtWidgets.QPushButton('Load image')
        layout.addWidget(self.loadImageButton, 0, 0, 1, 2)

        self.clearButton = QtWidgets.QPushButton('Clear')
        layout.addWidget(self.clearButton, 0, 2, 1, 1)
        
        self.saveChangesButton = QtWidgets.QPushButton('Save changes')
        layout.addWidget(self.saveChangesButton, 0, 4, 1, 2)



        self.actionLabel = QtWidgets.QLabel()
        layout.addWidget(self.actionLabel, 2, 2, 1, 2)
        self.actionLabel.setText("Load a file to get started")
        self.actionLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.nextImageButton = QtWidgets.QPushButton('>')
        layout.addWidget(self.nextImageButton, 1, 4)
        self.nextImageButton.setMinimumSize(20,IMAGE_HEIGHT)

        self.prevImageButton = QtWidgets.QPushButton('<')
        layout.addWidget(self.prevImageButton, 1, 1)
        self.prevImageButton.setMinimumSize(20,IMAGE_HEIGHT)


        self.loadImageButton.clicked.connect(self.loadImage)
        self.clearButton.clicked.connect(self.clearScene)
        self.saveChangesButton.clicked.connect(self.cropImage)
        self.nextImageButton.clicked.connect(self.nextImage)
        self.prevImageButton.clicked.connect(self.nextImage)

        self.filename = ''
        self.dirIterator = None
        self.fileList = []
        self.fullFileList = []
        self.pixmap = QtGui.QPixmap()

    def loadImage(self):
        self.actionLabel.setText("Select an Area to Crop")
        self.clearScene()
        self.filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select Image', '', 'Image Files (*.png *.jpg *.jpeg)')
        if self.filename:
            self.setWindowTitle(self.filename)
            self.pixmap = QtGui.QPixmap(self.filename).scaled(self.label.size(), 
                QtCore.Qt.KeepAspectRatio)
            if self.pixmap.isNull():
                return
            # self.label.graphicsPixmapItem = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(self.pixmap))
            # self.label.scene.addItem(self.label.graphicsPixmapItem)
            self.clearScene()
            dirpath = os.path.dirname(self.filename)
            self.fileList = []
            self.fullFileList = []
            for f in os.listdir(dirpath):
                fpath = os.path.join(dirpath, f)
                if os.path.isfile(fpath) and f.endswith(('.png', '.jpg', '.jpeg')):
                    self.fullFileList.append(fpath)
                for type in types:
                    key = '_' + type + '_'
                    if f.find(key) != -1: # find which type
                        if viewingImage[type] != '0': # has more than one channel
                            if viewingImage[type] == f[-5]:
                                self.fileList.append(fpath)
                        else: # only one channel
                            # print(f)
                            self.fileList.append(fpath)
                        break




            self.fileList.sort()
            self.fullFileList.sort()
            self.dirIterator = iter(self.fileList)
            try:
                while True:
                    # cycle through the iterator until the current file is found
                    if os.path.basename(next(self.dirIterator)) == os.path.basename(self.filename): # windows uses '\'
                        break
            except:
                # self.filename = next(self.dirIterator)
                self.actionLabel.setText('Warning: Channel being viewed is not the designated one for the type')

        

    def nextImage(self):
        if self.fileList:
            try:
                self.filename = next(self.dirIterator)
                self.setWindowTitle(self.filename)
                self.pixmap = QtGui.QPixmap(self.filename).scaled(self.label.size(), 
                    QtCore.Qt.KeepAspectRatio)
                if self.pixmap.isNull():
                    # the file is not a valid image, remove it from the list
                    # and try to load the next one
                    self.fileList.remove(self.filename)
                    self.nextImage()
                else:
                    self.clearScene()
            except:
                # the iterator has finished, restart it
                self.dirIterator = iter(self.fileList)
                self.nextImage()
        else:
            # no file list found, load an image
            self.loadImage()

        self.actionLabel.setText("Select an Area to Crop")

    def clearScene(self):
        # print('clearing')
        self.label.scene.clear()
        self.label.setAlignment(QtCore.Qt.AlignTop)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.graphicsPixmapItem = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(self.pixmap))
        self.label.scene.addItem(self.label.graphicsPixmapItem)

    
    def cropImage(self):
        base = self.filename[:self.filename.find('_s') + 3]
        for f in self.fullFileList:
            if f.find(base) != -1: #contains base
                # print('base =', base, 'cropping', f)
                im = Image.open(f)
                # print('im format:', im.format, 'dpi', im.info['dpi'])
                width, height = im.size
                ratio = width / self.pixmap.width()
                x1 = int(self.label.selectedRegion['x'] * ratio)
                y1 = int(self.label.selectedRegion['y'] * ratio)
                x2 = min(width, int((self.label.selectedRegion['w'] + self.label.selectedRegion['x']) * ratio))
                y2 = min(height, int((self.label.selectedRegion['h'] + self.label.selectedRegion['y']) * ratio))
                im1 = im.crop((x1,y1,x2,y2))
                # im1 = im.crop((int(self.label.selectedRegion['x'] * ratio), 
                #                int(self.label.selectedRegion['y'] * ratio), 
                #                int((self.label.selectedRegion['w'] + self.label.selectedRegion['x']) * ratio), 
                #                int((self.label.selectedRegion['h'] + self.label.selectedRegion['y']) * ratio)))
                # print('im1 format:', im.format, im.info['dpi'])
                im1.save(f, format = 'JPEG', dpi = im1.info['dpi'])#, quality = 'keep')
        self.pixmap = QtGui.QPixmap(self.filename).scaled(self.label.size(), 
                    QtCore.Qt.KeepAspectRatio)
        self.clearScene()

        

        



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    imageLoader = ImageLoader()
    imageLoader.show()
    sys.exit(app.exec_())