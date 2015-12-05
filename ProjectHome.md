Energy Plus is a building simulation suite.

http://apps1.eere.energy.gov/buildings/energyplus/

This software is to create and edit building description files.

# Thursday September 10, 2009 #

Uploaded version 0.1 of the idf editor. See below for the software dependancies. This only works with Energy Plus IDF files version 3.1.

Known Issue: On some platforms the file dialog is unstable and crashes.

To run the software, after extracting all the files into a folder, run:
```
python idfeditor.py
```

# Saturday, September 5, 2009 #

The basic functionality to create and edit and save idf files is implemented. Check out the svn tree and run python idfeditor.py. The software allows you to:

  * Open a version 3.1 idf file.
  * View and edit the classes.
  * Write an idf file.
  * Create a new object.
  * Load existing objects and their dependencies from an idf file for insertion into project.
  * Structured editing of Schedule:Compact.
  * Sort and query objects.
  * With the assorted field types it can
    * Integer and Real fields edited with spin boxes
    * Object-List fields allow selection of existing objects based on reference type
    * Choice fields offer a dropdown list of indicated choices
  * Extensible classes automatically add fields as required when editing.

A python script reads the IDD file and creates python classes for each defined EP object. Memos and notes are read and used for tooltips. These classes and their fields are subclasses, which allow data validity checking, special editors etc. to be defined.

The plan is to continue testing the current state and put together a release. The development is being done on Linux. Testing has not been done on Windows or OSX, and any assistance would be appreciated. Contact me at derekkite@gmail.com.

The software requires [Python](http://www.python.org/download/) and [PyQt](http://www.riverbankcomputing.co.uk/software/pyqt/intro), and the [Qt library](http://qt.nokia.com/).

Now for some screenshots.

http://picasaweb.google.ca/lh/photo/ZBcIAIvGwkBlXEAopPWkJQ?feat=directlink

![http://lh6.ggpht.com/_EnbYhFBB4vw/SqMZWFbWLNI/AAAAAAAAAjs/XHf8Rb-WIMQ/s144/energyplus-frontend1.png](http://lh6.ggpht.com/_EnbYhFBB4vw/SqMZWFbWLNI/AAAAAAAAAjs/XHf8Rb-WIMQ/s144/energyplus-frontend1.png)

http://picasaweb.google.ca/lh/photo/Ih5BqEKEEELPx5S1q-onjw?feat=directlink

![http://lh6.ggpht.com/_EnbYhFBB4vw/SqMZWMB-yGI/AAAAAAAAAjw/btaaleWS9BA/s144/energyplus-frontend2.png](http://lh6.ggpht.com/_EnbYhFBB4vw/SqMZWMB-yGI/AAAAAAAAAjw/btaaleWS9BA/s144/energyplus-frontend2.png)

http://picasaweb.google.ca/lh/photo/-ech06MG7ITCb6q5MTryZw?feat=directlink

![http://lh5.ggpht.com/_EnbYhFBB4vw/SqMZWRsgzgI/AAAAAAAAAj0/ZeV_X1PoFKM/s144/energyplus-frontend3.png](http://lh5.ggpht.com/_EnbYhFBB4vw/SqMZWRsgzgI/AAAAAAAAAj0/ZeV_X1PoFKM/s144/energyplus-frontend3.png)

http://picasaweb.google.ca/lh/photo/_V-csP-PtWlRvgYKK4_dFw?feat=directlink

![http://lh4.ggpht.com/_EnbYhFBB4vw/SqMZWYJHDPI/AAAAAAAAAj4/tupyGQelplU/s144/energyplus-frontend4.png](http://lh4.ggpht.com/_EnbYhFBB4vw/SqMZWYJHDPI/AAAAAAAAAj4/tupyGQelplU/s144/energyplus-frontend4.png)

Future:

The intent of the project is to allow building a simulation with some ease. The first phase is to build the data structures and allow editing individual objects. We are close to that goal.

Next is to allow easy creation of the simulation input data. Some things I have in mind:

Creation of Construction elements from the Energy Plus example and datasets provided in the installation.

Quick outline of building and zones, for a quick takeoff from drawings or sketches on site. By no means a drawing or CAD application, but some means of easily entering the zone and building dimensions.
