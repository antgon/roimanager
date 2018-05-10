import numpy as np

class ZoomDragManager:
    def __init__(self, ax):
        self.canvas = ax.figure.canvas
        self.ax = ax

    #def draw(self):
        #self.canvas.draw()

    def connect(self):
        im = self.ax.images[0]
        xmin, self.xmax, self.ymax, ymin = im.get_extent()
        self.cid_scroll = self.canvas.mpl_connect('scroll_event',\
                self.on_zoom)
        self.cid_press = self.canvas.mpl_connect('button_press_event',\
                self.on_press)
        self.cid_release = self.canvas.mpl_connect('button_release_event',\
                self.on_release)
        
    def disconnect(self):
        self.canvas.mpl_disconnect(self.cid_scroll)
        self.canvas.mpl_disconnect(self.cid_press)
        self.canvas.mpl_disconnect(self.cid_release)

    def on_press(self, event):
        '''
        If the user clicks and releases the mouse without scrolling,
        zoom image. If the user clicks-and-drags, then do not zoom but
        move the image around instead.
        '''
        if event.inaxes is None: return
        # A flag to know if the pointer was moved.
        self.ismotion = False
        # Consider dragging the image only if the left button was clicked.
        if event.button == 1:
            # Keep a reference to the point where the movement started.
            self.x0, self.y0 = event.xdata, event.ydata
            self.cid_motion = self.canvas.mpl_connect('motion_notify_event',\
                    self.on_motion)
        
    def on_release(self, event):
        '''
        Zoom in/out will be triggered by releasing the button,
        but only if no mouse dragging was done.
        '''
        self.canvas.mpl_disconnect(self.cid_motion)
        if not self.ismotion: self.on_zoom(event)
        
    def on_motion(self, event):
        if event.inaxes is None: return
        # if image is shown in full: return
        xmin, xmax = self.ax.get_xlim() 
        ymax, ymin = self.ax.get_ylim()
        xmin -= event.xdata-self.x0
        xmax -= event.xdata-self.x0
        ymin -= event.ydata-self.y0
        ymax -= event.ydata-self.y0
        # If the movement was too small it was probably unintended --
        # or the pen/tablet was used, which is very sensitive to small
        # movements and thus triggers dragging when trying to zoom in
        # by pressing against the tablet. To avoid this, ignore all
        # motion that is too small (in proportion to axes limits).
        if np.abs(event.xdata-self.x0)/(xmax-xmin) < 2e-3 \
                and \
                np.abs(event.ydata-self.y0)/(ymax-ymin) < 2e-3:
                    return
        self.ismotion = True
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymax, ymin)
        self.canvas.draw()

    def on_zoom(self, event):
        if self.canvas.widgetlock.locked(): return
        if event.inaxes is None: return
        # The image zoomed in or out will be centered about the clicked
        # point.
        cx, cy = event.xdata, event.ydata
        # The current limits of the image will be used to calculate the
        # new limits.
        xmin, xmax = self.ax.get_xlim() 
        ymax, ymin = self.ax.get_ylim()

        factor = 0.75
        # Left button pressed/scroll up = zoom in.
        if event.button == 1 or event.button == 'up':
            # At each click the image should be zoomed into by twice its
            # size along each dimension; ie new axes limits will span half
            # the length of the current ones.
            dx, dy = xmax-xmin, ymax-ymin
            # The zoomed-in area will be centred about the clicked point.
            xmin, xmax = cx - dx*(factor/2), cx + dx*(factor/2)
            
            # These lines are to avoid plotting beyond the limits of the
            # image while keeping the same x/y ratio.
            if xmin < 0: xmin, xmax = 0, dx*factor
            if xmax > self.xmax:
                xmax = self.xmax
                xmin = xmax - dx*factor
            ymin, ymax = cy - dy*factor/2, cy + dy*factor/2
            if ymin < 0: ymin, ymax = 0, dy*factor
            if ymax > self.ymax:
                ymax = self.ymax
                ymin = ymax - dy*factor

        # Right button pressed/scroll down = zoom out.
        elif event.button == 3 or event.button == 'down':
            # The new axes limits will be twice as long in each dimension
            # as the current ones, and centered about the clicked point.
            dx, dy = xmax-xmin, ymax-ymin
            xmin, xmax = cx-dx, cx+dx

            # As above, if the new limits go beyond the image limits,
            # the are is shifted to within the image limits while 
            # keeping the same x/y ratio.
            if xmin < 0: xmin, xmax = 0, dx*2
            if xmax > self.xmax:
                xmax = self.xmax
                xmin = np.max([0, xmax-dx*2])
            ymin, ymax = cy-dy, cy+dy
            if ymin < 0:
                ymin, ymax = 0, np.min([self.ymax, dy*2])
            if ymax > self.ymax:
                ymax = self.ymax
                ymin = np.max([0, ymax-dy*2])

        # Set new axes limits.
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymax, ymin)
        self.canvas.draw()
