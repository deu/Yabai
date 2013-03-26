from PyQt4.QtCore import Qt
from PyQt4.QtGui import QBrush, QColor, QGraphicsEllipseItem, QGraphicsRectItem, QPainter, QPen


class Shape:

    def __init__(self, item, imageWidth, imageHeight):

        super().__init__(item['x'], item['y'], item['w'], item['h'])

        self.imageWidth = imageWidth
        self.imageHeight = imageHeight

        self.x = item['x']; self.y = item['y']; self.w = item['w']; self.h = item['h']
        self.text = item['text']

        self.style = {}
        self.style['backgroundColor'] = item['style'].get('background-color', Qt.transparent)
        self.style['borderColor']     = item['style'].get('border-color'    , Qt.transparent)
        self.style['borderWidth']     = item['style'].get('border-width'    , 0)
        self.style['textColor']       = item['style'].get('text-color'      , '#000000')
        self.style['textFont']        = item['style'].get('text-font'       , None)
        self.style['textSize']        = item['style'].get('text-size'       , 1)
        self.style['textStyle']       = item['style'].get('text-style'      , '').split(' ')
        self.style['rotate']          = item['style'].get('rotate'          , 0)

        self.style['textAlignment'] = 0
        textAlignment = item['style'].get('text-align', 'hcenter vcenter').split(' ')
        if 'left'    in textAlignment: self.style['textAlignment'] |= Qt.AlignLeft
        if 'right'   in textAlignment: self.style['textAlignment'] |= Qt.AlignRight
        if 'hcenter' in textAlignment: self.style['textAlignment'] |= Qt.AlignHCenter
        if 'justify' in textAlignment: self.style['textAlignment'] |= Qt.AlignJustify
        if 'top'     in textAlignment: self.style['textAlignment'] |= Qt.AlignTop
        if 'bottom'  in textAlignment: self.style['textAlignment'] |= Qt.AlignBottom
        if 'vcenter' in textAlignment: self.style['textAlignment'] |= Qt.AlignVCenter

        self.setBrush(QBrush(QColor(self.style['backgroundColor'])))
        self.setRotation(self.style['rotate'])


    def paint(self, painter, *args, **kwargs):

        painter.setRenderHint(QPainter.Antialiasing)
        super().paint(painter, *args, **kwargs)

        # Draw the text (size relative to the height of the image):
        font = painter.font()
        font.setPixelSize((self.imageHeight / 100) * self.style['textSize'])
        font.setFamily(self.style['textFont'])
        if 'bold'      in self.style['textStyle']: font.setBold(True)
        if 'italic'    in self.style['textStyle']: font.setItalic(True)
        if 'underline' in self.style['textStyle']: font.setUnderline(True)
        painter.setFont(font)
        painter.setPen(QPen(QColor(self.style['textColor'])))
        painter.drawText(self.rect(), self.style['textAlignment'], self.text)


    def resize(self, imageWidth, imageHeight):

        self.imageWidth = imageWidth
        self.imageHeight = imageHeight

        # Resize the item:
        x = (self.imageWidth  / 100) * self.x
        y = (self.imageHeight / 100) * self.y
        w = (self.imageWidth  / 100) * self.w
        h = (self.imageHeight / 100) * self.h
        self.setRect(x, y, w, h)

        # Adjust the item's border width:
        pen = QPen(QColor(self.style['borderColor']))
        pen.setWidth((self.imageHeight / 100) * self.style['borderWidth'])
        self.setPen(pen)

        # Set the item's transform origin point (the point around which the item is
        # rotated by setRotation(), among other things) to its center:
        self.setTransformOriginPoint(self.boundingRect().x() + (self.boundingRect().width()  / 2),
                                     self.boundingRect().y() + (self.boundingRect().height() / 2))


class Ellipse(Shape, QGraphicsEllipseItem):
    pass


class Rectangle(Shape, QGraphicsRectItem):
    pass
