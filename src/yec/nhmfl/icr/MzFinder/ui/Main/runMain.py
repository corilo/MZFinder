'''
Created on May 13, 2015

@author: corilo
'''
import csv
import sys

from PySide.QtCore import SIGNAL
from PySide.QtGui import QMainWindow, QFileDialog, QTreeWidgetItem, QIcon, QPixmap, QMessageBox

from res import MainRes
from yec.nhmfl.icr.MzFinder.Inputs.Import_FTMS_Thermo.Load_FTMS_Thermo_File import ImportThermoFile
from yec.nhmfl.icr.MzFinder.Output.MzMatches2Excel import MzMatches_To_Report
from yec.nhmfl.icr.MzFinder.ui import run_Add_mz_dialog
from yec.nhmfl.icr.MzFinder.ui.Main.MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
        nativo = False
        tof_is_open = False
        icr_is_open = False
        hplc_is_open = False
        
        def __init__(self, parent=None):
            QMainWindow.__init__(self, parent)
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.connect(self.ui.actionOpen_Thermo_raw, SIGNAL("triggered()"), self.add_file)
            #QtCore.QObject.connect(self.ui.actionOpen_Thermo_raw, QtCore.SIGNAL("released()"), MainWindow.add_file)
        
        def add_file(self):
            
            arquivo_Caminhos = QFileDialog.getOpenFileNames(None,
                                    "Select Thermo *.raw files",
                                    '/',
                                    "(*.raw);; All Files (*.*)" , None)
            
            print arquivo_Caminhos
            for caminho in arquivo_Caminhos[0]:
                
                self.ui.listWidget.addItem(caminho)
                print caminho
            
        def delete_file(self):
            
            listItems= self.ui.listWidget.selectedItems()
            if not listItems: return        
            for item in listItems:
                self.ui.listWidget.takeItem(self.ui.listWidget.row(item))
        
        def add_mz(self):
            self.add_mz_dialog = run_Add_mz_dialog.run(self.ui.treeWidget)
            
            
        def delete_mz(self):
            
            for item in self.ui.treeWidget.selectedItems():
                
                index = self.ui.treeWidget.indexOfTopLevelItem(item)
                self.ui.treeWidget.takeTopLevelItem(index)
            
        def import_from_text_file(self):
            arquivo_Caminho = QFileDialog.getOpenFileName(None,
                                    "Select txt file",
                                    '/',
                                    "(*.txt);; All Files (*.*)" , None)[0]
                                    
            filename = arquivo_Caminho
            
            self.f = open(filename)
            
            reader = csv.reader(self.f, delimiter='\t')
            
            linhas = [linha for linha in reader]
            
            for i in linhas:
                if len(i) == 0:
                    continue
                else:
                    print i
                    a = QTreeWidgetItem(self.ui.treeWidget)
                    a.setText(0, str(i[0]))
                    a.setText(1, str(i[1]))
                    a.setText(2, str(i[2]))
                    a.setText(3, str(i[3]))
                        
            
        def process_clicked(self):
            
            dict_result = {}
            
            list_file_name = []
            for index in xrange(self.ui.listWidget.count()):
                
                arquivo = self.ui.listWidget.item(index).text()
                list_file_name.append(arquivo)
            
            list_of_tuples_mass_and_windows = []
            for index in xrange(self.ui.treeWidget.topLevelItemCount()):
                
                item = self.ui.treeWidget.topLevelItem(index)
                
                list_of_tuples_mass_and_windows.append((float(item.text(0)), float(item.text(1)), float(item.text(2).split(",")[0]), str(item.text(2).split(",")[1])))
                
            
            list_of_tuples_mass_and_windows_thresould = self.RemoveRepetidosLista(list_of_tuples_mass_and_windows)
            
            find_peaks = ImportThermoFile(list_of_tuples_mass_and_windows_thresould, list_file_name, dict_result)
            
            find_peaks.start()
            
            find_peaks.join()    
            
            icon_reader = QIcon(":/icons/images/find.png")
            icon_readerII = QPixmap(":/icons/images/find.png")
            message = QMessageBox()
                    
            if len(dict_result.keys()) > 0:
                
                try:
                    MzMatches_To_Report(dict_result)
                    
                    message.setIconPixmap(icon_readerII)
                    message.setText('Success')
                    message.setWindowIcon(icon_reader)
                    message.setWindowTitle("Success")
                    message.exec_()
                
                except:
                    
                    message.setIconPixmap(icon_readerII)
                    message.setText('Ups something went wrong')
                    message.setWindowIcon(icon_reader)
                    message.setWindowTitle("Success")
                    message.exec_()
                
            else:
                
                message.setIconPixmap(icon_readerII)
                message.setText('Sorry no matches found')
                message.setWindowIcon(icon_reader)
                message.setWindowTitle("No matches")
                message.exec_()    
        
        def RemoveRepetidosLista(self, lista):
            
            list2 = []    
            [list2.append(i) for i in lista if not i in list2] 
            return  list2
        
def run(app):
        
        #print QtGui.QStyleFactory.keys()
        
        #app.setStyle('WindowsVista')
        
        #pixmap = QtGui.QPixmap(":/images/logos/startup_bannerDemoI5-2.png")
        #splash = QtGui.QSplashScreen(pixmap)
        #splash.setMask(pixmap.mask())
        
        #splash.show()
        #splash.showMessage("(Only imageset editing implemented!) | Version: pre-release", QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter, QtCore.Qt.GlobalColor.blue)
        #for i in range(20):
        #    app.processEvents()
        #    time.sleep(0.2)

        
        
        f = MainWindow()
        #f.resize(1100, 600) 
        #f.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        f.show()
        #splash.finish(f)
        sys.exit(app.exec_())
                     