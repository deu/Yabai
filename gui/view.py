from PyQt4.QtCore import Qt, QSize
from PyQt4.QtGui import QBrush, QColor, QFontDatabase, QFrame, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView, QPixmap

from core.config import Config
from core.oshiri import Oshiri
import gui.shapes as shapes


class View(QGraphicsView):

    fitModes = {'view_fitBest', 'view_fitWidth', 'view_fitHeight', 'view_fitSize'}

    def __init__(self, fileName, fitMode):

        super().__init__()

        self.setFrameShape(QFrame.NoFrame)
        self.fitMode = fitMode
        self.setBackgroundBrush(QBrush(QColor(Config.backgroundColor)))
        self.openFile(fileName)


    def openFile(self, fileName):

        self.oshiri = Oshiri(fileName, 'r')
        self.loadFonts()

        self.page = 0
        self.display(self.oshiri.index[self.page])


    def display(self, page):

        scene = QGraphicsScene()
        self.setScene(scene)

        self.originalImage = QPixmap()
        self.originalImage.loadFromData(self.oshiri.getImage(page['image']))
        self.image = self.scene().addPixmap(self.originalImage)

        self.contents = page['contents']
        self.elements = []
        for item in page['contents']:
            shape = item['style'].get('shape', 'rectangle')
            shapeArgs = (item, self.image.pixmap().width(), self.image.pixmap().height())
            if   shape == 'ellipse':   newItem = shapes.Ellipse(*shapeArgs)
            elif shape == 'rectangle': newItem = shapes.Rectangle(*shapeArgs)
            self.elements.append(newItem)
            self.scene().addItem(newItem)

        self.updateView()


    def resizeEvent(self, sizes):

        super().resizeEvent(sizes)
        self.updateView()


    def setFitMode(self, mode):

        self.fitMode = mode

        self.updateView()

        if self.fitMode == 'view_fitWidth':
            self.centerOn(0, 0)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        else:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        Config.checkedActions ^= __class__.fitModes
        Config.checkedActions.add(self.fitMode)


    def scaleImage(self):

        self.scaledImage = self.originalImage

        if self.fitMode != 'view_fitSize':
            self.scaledImage = {
                'view_fitBest':   self.originalImage.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation),
                'view_fitWidth':  self.originalImage.scaledToWidth(self.width(), Qt.SmoothTransformation),
                'view_fitHeight': self.originalImage.scaledToHeight(self.height(), Qt.SmoothTransformation)
            }[self.fitMode]

        self.image.setPixmap(self.scaledImage)

        self.imageWidth = self.image.pixmap().width()
        self.imageHeight = self.image.pixmap().height()


    def updateView(self):

        self.scaleImage()

        self.scene().setSceneRect(0, 0, self.imageWidth, self.imageHeight)

        for element in self.elements:
            element.resize(self.imageWidth, self.imageHeight)


    def loadFonts(self):

        for font in self.oshiri.getFonts():
            QFontDatabase().addApplicationFontFromData(font)


    def previousPage(self):

        if self.page > 0: self.page -= 1
        self.display(self.oshiri.index[self.page])


    def nextPage(self):

        if self.page < len(self.oshiri.index) - 1: self.page += 1
        self.display(self.oshiri.index[self.page])
