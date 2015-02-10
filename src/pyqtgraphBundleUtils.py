# pyqtgraph bundle utility
#
# Copyright (C) 2012 Christian Gavin
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import os
import sys
from zipfile import ZipFile
from PyQt4 import QtGui
def myListdir(pathString):
    components = os.path.normpath(pathString).split(os.sep)
    # go through the components one by one, until one of them is a zip file
    for item in enumerate(components):
        index = item[0]
        component = item[1]
        (root, ext) = os.path.splitext(component)
        if ext == ".zip":
            results = []
            zipPath = os.sep.join(components[0:index+1])
            archivePath = components[index+1:]
            zipobj = ZipFile(zipPath, "r")
            contents = zipobj.namelist()
            zipobj.close()
            for name in contents:
                # components in zip archive paths are always separated by forward slash
                nameComponents = name.split("/")
                if nameComponents[0:-1] == archivePath:
                    results.append(nameComponents[-1].replace(".pyc", ".py"))
            return results
        else:
            return previousListDir(pathString)

previousListDir = os.listdir
os.listdir = myListdir
#-----------------------------------------------------------------------------
# look for bitmaps in current working directory
QtGui.QPixmap.oldinit = QtGui.QPixmap.__init__
def newinit(self, filename):
    # if file is not found inside the pyqtgraph package, look for it
    # in the current directory
    if not os.path.exists(filename):
        (root, tail) = os.path.split(filename)
        filename = os.path.join(os.getcwd(), tail)
    QtGui.QPixmap.oldinit(self, filename)

QtGui.QPixmap.__init__ = newinit
#-----------------------------------------------------------------------------
# we need to remove local library paths from Qt
QtGui.QApplication.oldinit = QtGui.QApplication.__init__

def newAppInit(self, *args):
    QtGui.QApplication.oldinit(self, *args)
    if hasattr(sys, "frozen"):
        # on Windows, this will not hurt because the path just won't be there
        print "Removing /opt/local/share/qt4/plugins from path"
        self.removeLibraryPath("/opt/local/share/qt4/plugins")
        print "Library paths:"
        for aPath in self.libraryPaths():
            print aPath
    else:
        print "Application running within Python interpreter."

QtGui.QApplication.__init__ = newAppInit
