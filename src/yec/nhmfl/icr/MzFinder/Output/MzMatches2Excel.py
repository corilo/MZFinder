'''
Created on May 14, 2015

@author: corilo
'''
from PySide.QtGui import QFileDialog
from pyExcelerator.Workbook import Workbook


class MzMatches_To_Report():
    '''
    classdocs
    '''

    def __init__(self, dict_results):
        
        
        headers = ["File", "scan", "m/z", "Intensity","Resolving Power", "Baseline", "Noise", "Charge"]    

        
        filedialog = QFileDialog()
        arquivo_out = filedialog.getSaveFileName(\
                                        None,
                                        "Export to Excel",
                                        "",
                                        "*.xls")[0]
        
        if arquivo_out == str(u''):
            pass
        else:
            
            self.write_results(arquivo_out, dict_results, headers)
            
        
    def write_results(self, arquivo_out, dict_results, headers):
        
        wb = Workbook()
        
        
        for reference_mass in sorted(dict_results):
            
            ws_each = wb.add_sheet(str(reference_mass))
            
            ws_each.write(0, 0, "File")
            ws_each.write(0, 1, "scan")
            ws_each.write(0, 2, "m/z")
            ws_each.write(0, 3, "Intensity")
            ws_each.write(0, 4, "Resolving Power")
            ws_each.write(0, 5, "Baseline")
            ws_each.write(0, 6, "Noise")
            ws_each.write(0, 7, "Signal2Noise")
            ws_each.write(0, 8, "Charge")
            
            cada_lista_resultados = dict_results.get(reference_mass)
            
            
            for index in range(len(cada_lista_resultados)):
                
                cada = cada_lista_resultados[index]
                
                ws_each.write(2+index, 0, cada[7])
                ws_each.write(2+index, 1, cada[6])
                ws_each.write(2+index, 2, cada[0])
                ws_each.write(2+index, 3, cada[1])
                ws_each.write(2+index, 4, cada[2])
                ws_each.write(2+index, 5, cada[3])
                ws_each.write(2+index, 6, cada[4])
                ws_each.write(2+index, 7, cada[1]/cada[4])
                ws_each.write(2+index, 8, cada[5])
                                                         
        wb.save(arquivo_out)           