from PyQt5.QtCore import QPoint, QPointF, Qt, QTime, QTimer
from PyQt5.QtGui import QColor, QPainter, QPolygon, QPen, QMouseEvent
from PyQt5.QtWidgets import QApplication, QWidget

import sys
import time
import threading
import random

def RandomColor():
  """Generate and return a random color from 64 color calculated set, no zeros"""
  r = random.randint(1,4)
  g = random.randint(1,4)
  b = random.randint(1,4)
  return QColor( r*64-1, g*64-1, b*64-1 )

class Shape:
  """Base Shape object, all drawn objects derive from this"""
  def __init__(self, x, y, color):
    self.xStart = x
    self.yStart = y
    self.fColor = color
    return super().__init__()

class BRectShape(Shape):
  """Base Rectangular Shaped objects, all boxed shapes derive from this"""
  def __init__(self, x, y, width, height, color, borderColor, borderThickness=0, xRadius=0, yRadius=0):
    self.width = width
    self.height = height
    self.borderColor = borderColor
    self.borderThickness = borderThickness
    return super().__init__(x, y, color)

class Rectangle(BRectShape):
  """Rectangle object to draw"""
  def __init__(self, x, y, width, height, color, borderColor, borderThickness=0, xRadius=0, yRadius=0):
    self.xRadius = xRadius
    self.yRadius = yRadius
    return super().__init__(x, y, width, height, color, borderColor, borderThickness)
  def Render(self, qp, scale=1):
    #drawRoundedRect(int x, int y, int w, int h, qreal xRadius, qreal yRadius,
    #Qt::SizeMode mode = Qt::AbsoluteSize)
    p = QPen()
    p.setColor(self.borderColor)
    p.setWidth(self.borderThickness)
    p.setStyle(Qt.SolidLine)
    qp.setPen(p)
    qp.setBrush(self.fColor)
    qp.drawRoundedRect(self.xStart * scale, self.yStart * scale, self.width * scale, self.height * scale, self.xRadius * scale, self.yRadius * scale)

class Ellipse(BRectShape):
  """Ellipical object to draw"""
  def __init__(self, x, y, width, height, color, borderColor, borderThickness=0):
    return super().__init__(x, y, width, height, color, borderColor, borderThickness)
  def Render(self, qp, scale=1):
    #Qt::SizeMode mode = Qt::AbsoluteSize)
    p = QPen()
    p.setColor(self.borderColor)
    p.setWidth(self.borderThickness)
    p.setStyle(Qt.SolidLine)
    qp.setPen(p)
    qp.setBrush(self.fColor)
    qp.drawEllipse( self.xStart * scale, self.yStart * scale, self.width * scale, self.height * scale )

class CenteredEllipse(BRectShape):
  """Centered Ellipical object to draw - x, y represent center coordinate"""
  def __init__(self, x, y, width, height, color, borderColor, borderThickness=0):
    return super().__init__(x, y, width, height, color, borderColor, borderThickness)
  def Render(self, qp, scale=1):
    #Qt::SizeMode mode = Qt::AbsoluteSize)
    p = QPen()
    p.setColor(self.borderColor)
    p.setWidth(self.borderThickness)
    p.setStyle(Qt.SolidLine)
    qp.setPen(p)
    qp.setBrush(self.fColor)
    #Overload of drawEllipse uses QPoint() arg to draw a centered, not boxed ellipse
    qp.drawEllipse( QPoint( self.xStart * scale, self.yStart * scale), self.width/2 * scale, self.height/2 * scale )

class DrawerCanvas(QWidget):

    TimerColor = QColor(127, 0, 0) # Color of Nifty Sweep Timer indicator, example of static member, not instance

    def __init__(self, width, height, parent=None):
      super(DrawerCanvas, self).__init__(parent)

      self.time = QTime.currentTime()

      # Create and bind timeout callback for 20ms update rate invoke of Refresh methos        
      timer = QTimer(self)
      timer.interval = 20
      timer.timeout.connect(self.Refresh)
      timer.start(20)

      self.setWindowTitle("PDrawer")
      self.resize(width, height)
      self.scale = 1 # scaling member for rendered objects
      self.shapes = [] # object rendering collection
      self.lockShapes = threading.Lock() # explicit lock object for add/clear/access marshalling

      self.lastMouseClickValid_L = False # init to no valid click yet
      self.lastMouseClickValid_R = False # init to no valid click yet
      # Save actual last event, provides more than just position - future use TODO
      self.lastMouseClickEvent = QMouseEvent( QMouseEvent.MouseMove, QPointF(), Qt.MouseButton(), Qt.MouseButtons(), Qt.NoModifier )
      self.lastMouseClickEvent_L = QMouseEvent( QMouseEvent.MouseMove, QPointF(), Qt.MouseButton(), Qt.MouseButtons(), Qt.NoModifier )
      self.lastMouseClickEvent_R = QMouseEvent( QMouseEvent.MouseMove, QPointF(), Qt.MouseButton(), Qt.MouseButtons(), Qt.NoModifier )
      self.lastMouseMoveEvent = QMouseEvent( QMouseEvent.MouseMove, QPointF(), Qt.MouseButton(), Qt.MouseButtons(), Qt.NoModifier )

    def mouseMoveEvent(self,qMouseEvent):
      self.lastMouseMoveEvent = QMouseEvent( qMouseEvent )

    def mouseReleaseEvent(self,qMouseEvent):
      self.lastMouseClickEvent = QMouseEvent(qMouseEvent)
      if self.lastMouseClickEvent.button() == Qt.LeftButton:
          self.lastMouseClickEvent_L=self.lastMouseClickEvent
          self.lastMouseClickValid_L = True # A new L click is now valid
      elif self.lastMouseClickEvent.button() == Qt.RightButton:
          self.lastMouseClickEvent_R=self.lastMouseClickEvent
          self.lastMouseClickValid_R = True # A new R click is now valid
      
      #return super().mouseReleaseEvent()

    def getLastMouseClick_L( self, pos ):
      wasValid = self.lastMouseClickValid_L
      pos.setX(self.lastMouseClickEvent.pos().x()) # allows pos to be modified, not just reassigned, passed by ref but re-assignment paradox
      pos.setY(self.lastMouseClickEvent.pos().y()) # allows pos to be modified, not just reassigned, passed by ref but re-assignment paradox
      self.lastMouseClickValid_L = False
      return wasValid

    def getLastMouseClick_R( self, pos ):
        wasValid = self.lastMouseClickValid_R
        pos.setX(self.lastMouseClickEvent.pos().x()) # allows pos to be modified, not just reassigned, passed by ref but re-assignment paradox
        pos.setY(self.lastMouseClickEvent.pos().y()) # allows pos to be modified, not just reassigned, passed by ref but re-assignment paradox
        self.lastMouseClickValid_R = False
        return wasValid

    def Clear(self):
      self.lockShapes.acquire()
      try:
        self.shapes.clear()
      finally:
        self.lockShapes.release()
    def Refresh(self):
      self.update()
    def Test(self, t):
      w = random.uniform(100,200)
      h = random.uniform(100,200)
      x = random.uniform(0,self.width() - w)
      y = random.uniform(0,self.height() - h)
      self.Add(Rectangle(x, y, w, h, QColor(255, 0, 0), QColor(0,127,0),5,25,25))

    def paintEvent(self, event):
      side = min(self.width(), self.height())
      stime = QTime.currentTime().msec()

      painter = QPainter(self)
      painter.setRenderHint(QPainter.Antialiasing)
      #painter.translate(self.width() / 2, self.height() / 2)
      #painter.scale(side / 200.0, side / 200.0)

      painter.eraseRect( self.rect())
      painter.save()
      #New Pen, because we want to set multiple properties : color and width
      p = QPen(self.TimerColor)
      p.setWidth(10)
      # Use our pen
      painter.setPen( p )

      # Angle specified in 1/16th of a degree, so scale it up
      painter.drawArc(0, 0, 40, 40, 16.0 * 360 * stime / 1000, 120 * 16.0)
      painter.restore()

      #This be where object rendering happens, iter through obj collection
      self.lockShapes.acquire()
      try:
        for s in self.shapes:
          s.Render(painter, self.scale )
      finally:
        self.lockShapes.release()

    def Add(self, obj):
      self.lockShapes.acquire()
      try:
        self.shapes.append(obj)
      finally:
        self.lockShapes.release()

import time
import threading
#exit = False

class Drawer(threading.Thread):
  """description of class"""
  def run(self):
    app = QApplication(sys.argv)
    self.width = self._kwargs['w']
    self.height = self._kwargs['h']
    self.Window = DrawerCanvas(self.width,self.height)
    self.Window.show()
    app.exec()
  def Add(self, obj):
    self.Window.Add(obj)
  def Test(self, t):
    self.Window.Test(0)
  def Render(self):
    self.Window.Refresh()
  def Clear(self):
    self.Window.Clear()

class PDrawer(object):
  """Python QT5 Basic Drawer"""
  def __init__(self, width=800, height=600):
    #self.width = width
    #self.height = height
    self.drawer = Drawer(kwargs={'w':width,'h':height})
    self.drawer.start()
    return super().__init__()
  def Render(self):
    self.drawer.Render()
  def Clear(self):
    self.drawer.Clear()
  def setScales( self, s ):
    self.drawer.Clear() # Must clear, old objects will be "old" scale
    self.drawer.Window.scale = s

  def AddRectangle(self, x, y, width, height, fillColor, borderColor=QColor(0,0,0), borderThickness=0, xRadius=0, yRadius=0):
    self.drawer.Add( Rectangle( x, y, width, height, fillColor, borderColor, borderThickness, xRadius, yRadius ))
  def AddEllipse(self, x, y, width, height, fillColor, borderColor=QColor(0,0,0), borderThickness=0):
    self.drawer.Add( Ellipse( x, y, width, height, fillColor, borderColor, borderThickness ))
  def AddCenteredEllipse(self, x, y, width, height, fillColor, borderColor=QColor(0,0,0), borderThickness=0):
    self.drawer.Add( CenteredEllipse( x, y, width, height, fillColor, borderColor, borderThickness ))

  def Test(self, t):
    self.drawer.Test(t)
  def getLastMouseClick_R( self, pos ):
    return self.drawer.Window.getLastMouseClick_R( pos )
  def getLastMouseClick_L( self, pos ):
    return self.drawer.Window.getLastMouseClick_L( pos )
  def getLastMousePosition( self ):
    # !! Careful, might need marshalling if lastMouseEvent is being updated when this is invoked...so far so good
    return self.drawer.Window.lastMouseMoveEvent.pos()
