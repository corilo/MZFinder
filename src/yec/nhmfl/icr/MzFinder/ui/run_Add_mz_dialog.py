'''
Created on May 13, 2015

@author: corilo
'''
from PySide.QtGui import QDialog, QTreeWidgetItem

from Add_mz_dialog import Ui_Dialog


class AddMZ(QDialog):
        
        
        def __init__(self, treeWidget, parent=None):
            QDialog.__init__(self, parent)
            self.ui = Ui_Dialog()
            self.ui.setupUi(self)
            self.mz = self.ui.doubleSpinBox.value()
            self.window = self.ui.doubleSpinBox1.value()
            self.treeWidget  = treeWidget
        
        def aceitar(self):
            
            print 'ok'
            self.mz = self.ui.doubleSpinBox.value()
            self.window = self.ui.doubleSpinBox1.value()
            self.threshould = self.ui.doubleSpinBox_2.value()
            self.threshould_method = self.ui.comboBox.currentText()
            
            a = QTreeWidgetItem(self.treeWidget)
            a.setText(0, str(self.mz))
            a.setText(1, str(self.window))
            a.setText(2, str(self.threshould) + " , " + self.threshould_method)
            
            
        def aceitou(self):
            
            print 'ok'
            #self.mz = self.ui.doubleSpinBox.value()
            #self.window = self.ui.doubleSpinBox1.value()
            #self.aceitou = True
            
            
        def rejeitou(self):
            self.close()
        
def run(treeWidget):
        
        f = AddMZ(treeWidget)
        #f.resize(1100, 600) 
        #f.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        f.show()
        #splash.finish(f)
        return f
            
            
                