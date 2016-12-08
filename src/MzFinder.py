'''
Created on Apr 12, 2011

@author: Usuario
'''

import os
import sys

from PySide import QtGui

from yec.nhmfl.icr.MzFinder.ui.Main import runMain


if __name__ == '__main__':
    
    #for keys, item in sys.modules.iteritems():
    #    print keys, item
    #print os.environ.get('PROGRAMFILES')+ " (x86)\\Druva\\inSync\\amd64\\insyncse.dll"
    
    #sys.stdout = open('my_stdout.log', 'w')
    #sys.stderr = open('my_stderr.log', 'w')
    #print  os.path.expanduser("~")
    #Lock.check_date
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("MzFinder")
    app.setQuitOnLastWindowClosed(True)
    runMain.run(app)
  
    
 
