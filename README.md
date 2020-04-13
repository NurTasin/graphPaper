# GraphPaper
<marquee>A library based on tkinter for ploting graphs of equations.</marquee>

<h2>Usages</h2>
This Library Allows you to create a virtual graph paper in your python tkinter window.
You can plot a whole graph of any kind of equation or statistics.
<h2>Installation</h2>
Put this library at the root path of your project.<br>
<strong>This libary don't need any kind of installation at all.</strong><br>
<h2>Methodes and Classes</h2>
The class and functions and their usages are listed below:
GraphPaper(screenHeight,screenWidth,title) --> This is the class to declare a virtual graph paper instance.<br>
self.clrScr() --> This methode clears the graph paper screen.<br>
self.clrScr() --> This methode clears the graph paper screen.<br>
self.makeScr() --> This methode creates a graphPaper layout on the blank graph paper.<br>
self.wait(sec) --> This methode stops the progression of the graph paper for <sec> seconds. [Parameter:Type]=[sec:float]<br>
self.markMainPoint() --> This methode indicates the (0,0) point of the graph paper.<br>
self.mark(x,y) --> This methode draws a Dot on the (x,y) point of the graph paper. [Parameter:Type]=[x,y:float,float]<br>
self.joinDots() --> This methode joins the Dots on the graph paper according to their serial of marking on the paper.<br>
self.setPixelUnit(XUnit,YUnit) --> Sets the unit of X and Y axis accordingly . The unit is measured in pixels. [Parameter:Type]=[XUnit,YUnit:int,int]<br>
self.setColorOfLines(r,g,b) --> Sets the color of normal square lines in mixed form of RED,GREEN,BLUE paramed as r,g,b accordingly. [Parameter:Type]=[r,g,b:byte,byte,byte]<br>
self.waitUntilClick() --> Stops progress of graph paper until a click from mouse is detected.<br>
self.close() --> Closes the graph paper window properly.<br>
<br>
<h2>Conclusion</h2>
N.B: As this library is designed and built within 15~20 minutes you may find some bugs here. Issue it on https://github.com/NurTasin/graphPaper/issues .<br>
The module graphics.py I have used in this library, is open-source software released under the terms of the
GPL (http://www.gnu.org/licenses/gpl.html).<br><br>
<strong>Thanks to John Zelle and Others for designing the graphics library.</strong>
