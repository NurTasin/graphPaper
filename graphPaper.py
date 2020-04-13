"""
This Library Allows you to create a virtual graph paper in your python tkinter window.
You can plot a whole graph of any kind of equation or statistics.
The class and functions and their usages are listed below:
------------------------------------------------------------------
GraphPaper(screenHeight,screenWidth,title) --> This is the class to declare a virtual graph paper instance.

self.clrScr() --> This methode clears the graph paper screen.
self.makeScr() --> This methode creates a graphPaper layout on the blank graph paper.
self.wait(sec) --> This methode stops the progression of the graph paper for <sec> seconds. [Parameter:Type]=[sec:float]
self.markMainPoint() --> This methode indicates the (0,0) point of the graph paper.
self.mark(x,y) --> This methode draws a Dot on the (x,y) point of the graph paper. [Parameter:Type]=[x,y:float,float]
self.joinDots() --> This methode joins the Dots on the graph paper according to their serial of marking on the paper.
self.setPixelUnit(XUnit,YUnit) --> Sets the unit of X and Y axis accordingly . The unit is measured in pixels. [Parameter:Type]=[XUnit,YUnit:int,int]
self.setColorOfLines(r,g,b) --> Sets the color of normal square lines in mixed form of RED,GREEN,BLUE paramed as r,g,b accordingly. [Parameter:Type]=[r,g,b:byte,byte,byte]
self.waitUntilClick() --> Stops progress of graph paper until a click from mouse is detected.
self.close() --> Closes the graph paper window properly.

N.B: As this library is designed and built within 15~20 minutes you may find some bugs here. Issue it on www.github.com/NurTasin/graphPaper.git

The module graphics.py I have used in this library is open-source software released under the terms of the
GPL (http://www.gnu.org/licenses/gpl.html).
Thanks to John Zelle and Others for designing the graphics library.

"""

"""Embedding the needed objects or class and methodes from graphics.py"""
#graphics.py by John Zelle
import time, os, sys

try:  # import as appropriate for 2.x vs. 3.x
   import tkinter as tk
except:
   import Tkinter as tk

class GraphicsError(Exception):
    """Generic error class for graphics module exceptions."""
    pass

OBJ_ALREADY_DRAWN = "Object currently drawn"
UNSUPPORTED_METHOD = "Object doesn't support operation"
BAD_OPTION = "Illegal option value"

##########################################################################
# global variables and funtions

_root = tk.Tk()
_root.withdraw()

_update_lasttime = time.time()

def update(rate=None):
    global _update_lasttime
    if rate:
        now = time.time()
        pauseLength = 1/rate-(now-_update_lasttime)
        if pauseLength > 0:
            time.sleep(pauseLength)
            _update_lasttime = now + pauseLength
        else:
            _update_lasttime = now

    _root.update()

############################################################################
# Graphics classes start here
        
class GraphWin(tk.Canvas):

    """A GraphWin is a toplevel window for displaying graphics."""

    def __init__(self, title="Graphics Window",
                 width=200, height=200, autoflush=True):
        assert type(title) == type(""), "Title must be a string"
        master = tk.Toplevel(_root)
        master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Canvas.__init__(self, master, width=width, height=height,
                           highlightthickness=0, bd=0)
        self.master.title(title)
        self.pack()
        master.resizable(0,0)
        self.foreground = "black"
        self.items = []
        self.mouseX = None
        self.mouseY = None
        self.bind("<Button-1>", self._onClick)
        self.bind_all("<Key>", self._onKey)
        self.height = int(height)
        self.width = int(width)
        self.autoflush = autoflush
        self._mouseCallback = None
        self.trans = None
        self.closed = False
        master.lift()
        self.lastKey = ""
        if autoflush: _root.update()

    def __repr__(self):
        if self.isClosed():
            return "<Closed GraphWin>"
        else:
            return "GraphWin('{}', {}, {})".format(self.master.title(),
                                             self.getWidth(),
                                             self.getHeight())

    def __str__(self):
        return repr(self)
     
    def __checkOpen(self):
        if self.closed:
            raise GraphicsError("window is closed")

    def _onKey(self, evnt):
        self.lastKey = evnt.keysym


    def setBackground(self, color):
        """Set background color of the window"""
        self.__checkOpen()
        self.config(bg=color)
        self.__autoflush()
        
    def setCoords(self, x1, y1, x2, y2):
        """Set coordinates of window to run from (x1,y1) in the
        lower-left corner to (x2,y2) in the upper-right corner."""
        self.trans = Transform(self.width, self.height, x1, y1, x2, y2)
        self.redraw()

    def close(self):
        """Close the window"""

        if self.closed: return
        self.closed = True
        self.master.destroy()
        self.__autoflush()


    def isClosed(self):
        return self.closed


    def isOpen(self):
        return not self.closed


    def __autoflush(self):
        if self.autoflush:
            _root.update()

    
    def plot(self, x, y, color="black"):
        """Set pixel (x,y) to the given color"""
        self.__checkOpen()
        xs,ys = self.toScreen(x,y)
        self.create_line(xs,ys,xs+1,ys, fill=color)
        self.__autoflush()
        
    def plotPixel(self, x, y, color="black"):
        """Set pixel raw (independent of window coordinates) pixel
        (x,y) to color"""
        self.__checkOpen()
        self.create_line(x,y,x+1,y, fill=color)
        self.__autoflush()
      
    def flush(self):
        """Update drawing to the window"""
        self.__checkOpen()
        self.update_idletasks()
        
    def getMouse(self):
        """Wait for mouse click and return Point object representing
        the click"""
        self.update()      # flush any prior clicks
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            self.update()
            if self.isClosed(): raise GraphicsError("getMouse in closed window")
            time.sleep(.1) # give up thread
        x,y = self.toWorld(self.mouseX, self.mouseY)
        self.mouseX = None
        self.mouseY = None
        return Point(x,y)

    def checkMouse(self):
        """Return last mouse click or None if mouse has
        not been clicked since last call"""
        if self.isClosed():
            raise GraphicsError("checkMouse in closed window")
        self.update()
        if self.mouseX != None and self.mouseY != None:
            x,y = self.toWorld(self.mouseX, self.mouseY)
            self.mouseX = None
            self.mouseY = None
            return Point(x,y)
        else:
            return None

    def getKey(self):
        """Wait for user to press a key and return it as a string."""
        self.lastKey = ""
        while self.lastKey == "":
            self.update()
            if self.isClosed(): raise GraphicsError("getKey in closed window")
            time.sleep(.1) # give up thread

        key = self.lastKey
        self.lastKey = ""
        return key

    def checkKey(self):
        """Return last key pressed or None if no key pressed since last call"""
        if self.isClosed():
            raise GraphicsError("checkKey in closed window")
        self.update()
        key = self.lastKey
        self.lastKey = ""
        return key
            
    def getHeight(self):
        """Return the height of the window"""
        return self.height
        
    def getWidth(self):
        """Return the width of the window"""
        return self.width
    
    def toScreen(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.screen(x,y)
        else:
            return x,y
                      
    def toWorld(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.world(x,y)
        else:
            return x,y
        
    def setMouseHandler(self, func):
        self._mouseCallback = func
        
    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        if self._mouseCallback:
            self._mouseCallback(Point(e.x, e.y))

    def addItem(self, item):
        self.items.append(item)

    def delItem(self, item):
        self.items.remove(item)

    def redraw(self):
        for item in self.items[:]:
            item.undraw()
            item.draw(self)
        self.update()
        
                      
class Transform:

    """Internal class for 2-D coordinate transformations"""
    
    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        # w, h are width and height of window
        # (xlow,ylow) coordinates of lower-left [raw (0,h-1)]
        # (xhigh,yhigh) coordinates of upper-right [raw (w-1,0)]
        xspan = (xhigh-xlow)
        yspan = (yhigh-ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = xspan/float(w-1)
        self.yscale = yspan/float(h-1)
        
    def screen(self,x,y):
        # Returns x,y in screen (actually window) coordinates
        xs = (x-self.xbase) / self.xscale
        ys = (self.ybase-y) / self.yscale
        return int(xs+0.5),int(ys+0.5)
        
    def world(self,xs,ys):
        # Returns xs,ys in world coordinates
        x = xs*self.xscale + self.xbase
        y = self.ybase - ys*self.yscale
        return x,y


# Default values for various item configuration options. Only a subset of
#   keys may be present in the configuration dictionary for a given item
DEFAULT_CONFIG = {"fill":"",
      "outline":"black",
      "width":"1",
      "arrow":"none",
      "text":"",
      "justify":"center",
                  "font": ("helvetica", 12, "normal")}

class GraphicsObject:

    """Generic base class for all of the drawable objects"""
    # A subclass of GraphicsObject should override _draw and
    #   and _move methods.
    
    def __init__(self, options):
        # options is a list of strings indicating which options are
        # legal for this object.
        
        # When an object is drawn, canvas is set to the GraphWin(canvas)
        #    object where it is drawn and id is the TK identifier of the
        #    drawn shape.
        self.canvas = None
        self.id = None

        # config is the dictionary of configuration options for the widget.
        config = {}
        for option in options:
            config[option] = DEFAULT_CONFIG[option]
        self.config = config
        
    def setFill(self, color):
        """Set interior color to color"""
        self._reconfig("fill", color)
        
    def setOutline(self, color):
        """Set outline color to color"""
        self._reconfig("outline", color)
        
    def setWidth(self, width):
        """Set line weight to width"""
        self._reconfig("width", width)

    def draw(self, graphwin):

        """Draw the object in graphwin, which should be a GraphWin
        object.  A GraphicsObject may only be drawn into one
        window. Raises an error if attempt made to draw an object that
        is already visible."""

        if self.canvas and not self.canvas.isClosed(): raise GraphicsError(OBJ_ALREADY_DRAWN)
        if graphwin.isClosed(): raise GraphicsError("Can't draw to closed window")
        self.canvas = graphwin
        self.id = self._draw(graphwin, self.config)
        graphwin.addItem(self)
        if graphwin.autoflush:
            _root.update()
        return self

            
    def undraw(self):

        """Undraw the object (i.e. hide it). Returns silently if the
        object is not currently drawn."""
        
        if not self.canvas: return
        if not self.canvas.isClosed():
            self.canvas.delete(self.id)
            self.canvas.delItem(self)
            if self.canvas.autoflush:
                _root.update()
        self.canvas = None
        self.id = None


    def move(self, dx, dy):

        """move object dx units in x direction and dy units in y
        direction"""
        
        self._move(dx,dy)
        canvas = self.canvas
        if canvas and not canvas.isClosed():
            trans = canvas.trans
            if trans:
                x = dx/ trans.xscale 
                y = -dy / trans.yscale
            else:
                x = dx
                y = dy
            self.canvas.move(self.id, x, y)
            if canvas.autoflush:
                _root.update()
           
    def _reconfig(self, option, setting):
        # Internal method for changing configuration of the object
        # Raises an error if the option does not exist in the config
        #    dictionary for this object
        if option not in self.config:
            raise GraphicsError(UNSUPPORTED_METHOD)
        options = self.config
        options[option] = setting
        if self.canvas and not self.canvas.isClosed():
            self.canvas.itemconfig(self.id, options)
            if self.canvas.autoflush:
                _root.update()


    def _draw(self, canvas, options):
        """draws appropriate figure on canvas with options provided
        Returns Tk id of item drawn"""
        pass # must override in subclass


    def _move(self, dx, dy):
        """updates internal state of object to move it dx,dy units"""
        pass # must override in subclass

         
class Point(GraphicsObject):
    def __init__(self, x, y):
        GraphicsObject.__init__(self, ["outline", "fill"])
        self.setFill = self.setOutline
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)
        
    def _draw(self, canvas, options):
        x,y = canvas.toScreen(self.x,self.y)
        return canvas.create_rectangle(x,y,x+1,y+1,options)
        
    def _move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        
    def clone(self):
        other = Point(self.x,self.y)
        other.config = self.config.copy()
        return other
                
    def getX(self): return self.x
    def getY(self): return self.y

class _BBox(GraphicsObject):
    # Internal base class for objects represented by bounding box
    # (opposite corners) Line segment is a degenerate case.
    
    def __init__(self, p1, p2, options=["outline","width","fill"]):
        GraphicsObject.__init__(self, options)
        self.p1 = p1.clone()
        self.p2 = p2.clone()

    def _move(self, dx, dy):
        self.p1.x = self.p1.x + dx
        self.p1.y = self.p1.y + dy
        self.p2.x = self.p2.x + dx
        self.p2.y = self.p2.y  + dy
                
    def getP1(self): return self.p1.clone()

    def getP2(self): return self.p2.clone()
    
    def getCenter(self):
        p1 = self.p1
        p2 = self.p2
        return Point((p1.x+p2.x)/2.0, (p1.y+p2.y)/2.0)

class Line(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2, ["arrow","fill","width"])
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def __repr__(self):
        return "Line({}, {})".format(str(self.p1), str(self.p2))

    def clone(self):
        other = Line(self.p1, self.p2)
        other.config = self.config.copy()
        return other
  
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_line(x1,y1,x2,y2,options)
        
    def setArrow(self, option):
        if not option in ["first","last","both","none"]:
            raise GraphicsError(BAD_OPTION)
        self._reconfig("arrow", option)

class Text(GraphicsObject):
    
    def __init__(self, p, text):
        GraphicsObject.__init__(self, ["justify","fill","text","font"])
        self.setText(text)
        self.anchor = p.clone()
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def __repr__(self):
        return "Text({}, '{}')".format(self.anchor, self.getText())
    
    def _draw(self, canvas, options):
        p = self.anchor
        x,y = canvas.toScreen(p.x,p.y)
        return canvas.create_text(x,y,options)
        
    def _move(self, dx, dy):
        self.anchor.move(dx,dy)
        
    def clone(self):
        other = Text(self.anchor, self.config['text'])
        other.config = self.config.copy()
        return other

    def setText(self,text):
        self._reconfig("text", text)
        
    def getText(self):
        return self.config["text"]
            
    def getAnchor(self):
        return self.anchor.clone()

    def setFace(self, face):
        if face in ['helvetica','arial','courier','times roman']:
            f,s,b = self.config['font']
            self._reconfig("font",(face,s,b))
        else:
            raise GraphicsError(BAD_OPTION)

    def setSize(self, size):
        if 5 <= size <= 36:
            f,s,b = self.config['font']
            self._reconfig("font", (f,size,b))
        else:
            raise GraphicsError(BAD_OPTION)

    def setStyle(self, style):
        if style in ['bold','normal','italic', 'bold italic']:
            f,s,b = self.config['font']
            self._reconfig("font", (f,s,style))
        else:
            raise GraphicsError(BAD_OPTION)

    def setTextColor(self, color):
        self.setFill(color)

def color_rgb(r,g,b):
    """r,g,b are intensities of red, green, and blue in range(256)
    Returns color specifier string for the resulting color"""
    return "#%02x%02x%02x" % (r,g,b)

class Rectangle(_BBox):
    
    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def __repr__(self):
        return "Rectangle({}, {})".format(str(self.p1), str(self.p2))
    
    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1,y1 = canvas.toScreen(p1.x,p1.y)
        x2,y2 = canvas.toScreen(p2.x,p2.y)
        return canvas.create_rectangle(x1,y1,x2,y2,options)
        
    def clone(self):
        other = Rectangle(self.p1, self.p2)
        other.config = self.config.copy()
        return other
"""end of graphics.py"""


"""Start of Graphpaper Object"""
class GraphPaper():
	def __init__(self,screenHeight,screenWidth,title):
		self.Height=screenHeight
		self.Width=screenWidth
		self.Title=str(title)
		self.listOfLinesOfX=[]
		self.listOfLinesOfY=[]
		self.colorOfSubLines=color_rgb(0, 0, 0)
		self.win=GraphWin(str(title),screenWidth,screenHeight)
		self.pixelUnitX=10
		self.pixelUnitY=10
		self.nH=1
		self.nW=1
		self.listOfDots_=[]
		self.clrScr()

	def __str__(self):
		return "Graphpaper Object(Height={},Width={},Title=\"{}\")".format(self.Height,self.Width,self.Title)

	def __len__(self):
		return self.Height*self.Width

	def clrScr(self):
		self.listOfLinesOfX=[]
		self.listOfLinesOfY=[]
		rect=Rectangle(Point(0,0), Point(self.Width,self.Height))
		rect.setOutline(color_rgb(255,255,255))
		rect.setFill(color_rgb(255,255,255))
		rect.draw(self.win)

	def makeScr(self):
		for i in range(0,self.Width+1,self.pixelUnitX):
			line=Line(Point(i,0), Point(i,self.Height))
			if i%(5*self.pixelUnitX)==0:
				line.setOutline(color_rgb(0,0,255))
				line.setWidth(2)
			else:
				line.setOutline(self.colorOfSubLines)
			line.draw(self.win)
			self.listOfLinesOfX.append(line)

		for i in range(0,self.Height+1,self.pixelUnitY):
			line=Line(Point(0,i), Point(self.Width,i))
			if i%(5*self.pixelUnitX)==0:
				line.setOutline(color_rgb(0,0,255))
				line.setWidth(2)
			else:
				line.setOutline(self.colorOfSubLines)
			line.draw(self.win)
			self.listOfLinesOfY.append(line)

	def wait(self,time_):
		from time import sleep
		sleep(time_)
	
	def close(self):
		self.win.close()

	def markMainPoint(self):
		self.makeScr()
		self.nW=(self.Width//self.pixelUnitX)/2
		self.nH=(self.Height//self.pixelUnitY)/2
		line1=self.listOfLinesOfX[int(self.nW)]
		line2=self.listOfLinesOfY[int(self.nH)]
		line1.undraw()
		line2.undraw()
		line1.setOutline(color_rgb(0,0,0))
		line2.setOutline(color_rgb(0,0,0))

		line1.setWidth(2)
		line2.setWidth(2)

		line1.draw(self.win)
		line2.draw(self.win)

		labelY=Text(Point((int(self.nW)*self.pixelUnitX)-15,15),"Y")
		labelY.setTextColor(color_rgb(0,0,0))
		labelY.setSize(15)
		labelY.draw(self.win)

		labelYdash=Text(Point((int(self.nW)*self.pixelUnitX)-15,self.Height-15),"Y\'")
		labelYdash.setTextColor(color_rgb(0,0,0))
		labelYdash.setSize(15)
		labelYdash.draw(self.win)

		labelXdash=Text(Point(15,(int(self.nH)*self.pixelUnitY)+15), "X\'")
		labelXdash.setTextColor(color_rgb(0,0,0))
		labelXdash.setSize(15)
		labelXdash.draw(self.win)

		labelX=Text(Point(self.Width-15,(int(self.nH)*self.pixelUnitY)+15), "X")
		labelX.setTextColor(color_rgb(0,0,0))
		labelX.setSize(15)
		labelX.draw(self.win)
	def mark(self,x,y):
		x2=(x+int(self.nW))*self.pixelUnitX
		y2=(-y+int(self.nH))*self.pixelUnitY
		marker=Rectangle(Point(x2-0.75,y2-0.75), Point(x2+0.5,y2+0.5))
		marker.setOutline(color_rgb(255,0,0))
		marker.setFill(color_rgb(255,0,0))
		marker.setWidth(3)
		marker.draw(self.win)
		self.listOfDots_.append([x,y])

	def joinDots(self):
		listOfDots=self.listOfDots_
		for i in range(len(listOfDots)):
			global joiningLine
			if i!=len(listOfDots)-1:
				x1=(listOfDots[i][0]+int(self.nW))*self.pixelUnitX
				y1=(-listOfDots[i][1]+int(self.nH))*self.pixelUnitY

				x2=(listOfDots[i+1][0]+int(self.nW))*self.pixelUnitX
				y2=(-listOfDots[i+1][1]+int(self.nH))*self.pixelUnitY

				joiningLine=Line(Point(x1,y1), Point(x2,y2))
			if i==len(listOfDots)-1:
				x1=(listOfDots[i][0]+int(self.nW))*self.pixelUnitX
				y1=(-listOfDots[i][1]+int(self.nH))*self.pixelUnitY
				joiningLine=Line(Point(x1,y1), Point(x1,y1))
			joiningLine.setWidth(1)
			joiningLine.setOutline(color_rgb(255,0,0))
			joiningLine.draw(self.win)
	def setPixelUnit(self,XUnit,YUnit):
		self.pixelUnitX=int(XUnit)
		self.pixelUnitY=int(YUnit)
		self.clrScr()
		self.makeScr()
		self.markMainPoint()

	def setColorOfLines(self,r,g,b):
		self.colorOfSubLines=color_rgb(r, g, b)

	def waitUntilClick(self):
		self.win.getMouse()
"""End of GraphPaper Object"""
if __name__=="__main__":
	first=GraphPaper(700, 1300,"figure 1")
	first.setPixelUnit(10, 10)
	first.mark(-20,-20)
	print(str(first))
	print(len(first))
	first.wait(2)

	try:
		first.win.getMouse()
	except GraphicsError:
		pass
