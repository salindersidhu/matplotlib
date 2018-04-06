Implemented new zoom feature using mouse scroll wheel
-----------------------------------------------------

Matplotlib now supports the ability to zoom in and out of a plot using a
mouse scroll wheel. Scrolling the mouse wheel up will zoom into the plot at the
location of the cursor. Scrolling the mouse wheel down will zoom out the plot
at the location of the cursor. This feature works by modifying the axes view
limits, which is used with the existing zoom-to-rectangle functionality.

The ``Zoom-to-rectangle`` button has been renamed to ``Zoom`` because it 
supports zoom to point using the mouse scroll wheel along with the existing 
zoom to a rectangular region functionality.
