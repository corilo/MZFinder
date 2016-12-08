
from collections import namedtuple
from ctypes import c_double, c_long, c_int
from threading import Thread

from comtypes import CoInitialize
from comtypes.automation import VARIANT, BSTR
from comtypes.client import CreateObject, GetActiveObject
from numpy import array
import numpy
import pythoncom
import win32com.client


class ImportThermoFile(Thread):
    
    
    def __init__(self, list_of_tuples_mass_and_windows, list_file_name, dict_result ):
        
        Thread.__init__(self)
        
        '''Set up the COM object interface'''
        self.list_of_tuples_mass_and_windows = list_of_tuples_mass_and_windows
        self.list_file_name = list_file_name
        self.dict_result = dict_result
                
    def run(self):
        
                
            for file_location in self.list_file_name:
                
                CoInitialize()
                
                self.thermo_Library = CreateObject('MSFileReader.XRawfile')
                
                self.thermo_Library.open(file_location) 
                
                self.res = self.thermo_Library.SetCurrentController(0,1)
                
                if self.check_load_sucess():
                    
                    self.get_mass_spectrums(file_location)
                    
                else:
                    
                    self.break_it = True
                
                del self.thermo_Library      

    def check_load_sucess(self):
        
        ''' 0 if successful; otherwise, see Error Codes '''
        if self.res == 0:
            
            return True
        
        else:
            
            return False
        
    def get_polarity_mode(self, label):
        
        #print label
        polarity_symbel = label.value.split()[1]
        #print polarity_symbel
        if polarity_symbel == "+":
            
            return "POSITIVE_ION_MODE"
        
        elif polarity_symbel == "-":
        
            return "NEGATIVE_ION_MODE"
        
        else:
            
            return "Unknown"
        
    def get_A_B_ValueFromScanNum(self, nScans):
        
        A = c_long()
        B = c_long()
        D = c_double()
        pnNumMassCalibrators = c_int()
        n = c_int(2)
        self.thermo_Library.GetAValueFromScanNum(nScans, A)
        self.thermo_Library.GetBValueFromScanNum(nScans, B)
        
        if A and B == 0:
            return False, False
        #print A, B, D, n
        else:
            
            self.thermo_Library.GetNumberOfMassCalibratorsFromScanNum(nScans, pnNumMassCalibrators) 
            for i in range(pnNumMassCalibrators.value):
                self.thermo_Library.GetMassCalibrationValueFromScanNum(nScans,i, D)
                #print D.value
            
        return A.value, B.value, D.value, n.value
    
    def get_label_data(self, scan):
        
        scan = c_long(scan)
        pvarLabels = VARIANT()
        pvarFlags = VARIANT()
        
        self.thermo_Library.GetLabelData(pvarLabels, pvarFlags, scan)
        scans_labels = numpy.array(pvarLabels.value)
        
        mz =        scans_labels[0]
        magnitude = scans_labels[1]
        resolution =        scans_labels[2]
        base_noise = scans_labels[3]
        noise =        scans_labels[4]
        charge = scans_labels[5]
        
        return mz, magnitude, resolution, base_noise, noise, charge
    
    def get_scans_numbers(self):
        
        nScans = c_long()
        self.thermo_Library.GetNumSpectra(nScans)
        
        return nScans
    
    def get_initial_rt(self):
        
        initial_rt = c_double()
        self.thermo_Library.GetStartTime(initial_rt)
        
        return initial_rt.value
    
    def get_final_rt(self):
        
        final_rt = c_double()
        self.thermo_Library.GetEndTime(final_rt)
        
        return final_rt.value
    
    def get_scans_labels(self):
       
        out = VARIANT()
        arsize = c_long()
        self.thermo_Library.GetFilters(out, arsize)
        scans_labels = numpy.array(out.value)
        return scans_labels, arsize 
    
    def get_scans_labels_for_scan_number(self, scan_number):
        
        scan_label = BSTR()
        scan_number = c_long(scan_number)
        
        self.thermo_Library.GetFilterForScanNum(scan_number, scan_label)
        
        return scan_label 
                                        
    def get_segment_mass_list_from_scan_num(self, scan):
        
        data = array('f')
        
        scan = c_long(scan)
        scanFilter = u''
        scanIntensityCutoffType = c_long( 0) # 0 = none, 1=Abs, 2=Rel. to basepk
        scanIntensityCutoffValue = c_long( 0)
        scanMaxNumberOfPeaks = c_long( 0)
        scanCentroidResult = c_long( 0)
        dCentroidPeakWidth = c_double( 0)
        massList = VARIANT()
        peakFlags = VARIANT()
        arsize = c_long()
        varSegments = VARIANT()
        NumSegments = c_long()
        varMassRange = VARIANT()
        
        self.thermo_Library.GetSegmentedMassListFromScanNum(
                                          scan, scanFilter,
                                          scanIntensityCutoffType,
                                          scanIntensityCutoffValue,
                                          scanMaxNumberOfPeaks, scanCentroidResult,
                                          dCentroidPeakWidth,
                                          massList,peakFlags,
                                          arsize, varSegments,
                                          NumSegments,
                                          varMassRange)
        
        data = array(massList.value)
            
        return data[0], data[1]
    
    def get_mass_list_from_scan_num(self, scan, minmz, maxmz):
        
        '''init_variable_from_get_spectrums
        # massList set up later
        '''
        
        scan = c_long(scan)
        scanFilter = u''
        scanIntensityCutoffType = c_long( 0) # 0 = none, 1=Abs, 2=Rel. to basepk
        scanIntensityCutoffValue = c_long( 0)
        scanMaxNumberOfPeaks = c_long( 0)
        scanCentroidResult = c_long( 0)
        peakFlags = VARIANT() #Unused variable
        # massList set up later
        arsize = c_long()
        
        data = array('f')
        
        massList = VARIANT()
        self.thermo_Library.GetMassListFromScanNum(
                scan,scanFilter,
                scanIntensityCutoffType,
                scanIntensityCutoffValue,
                scanMaxNumberOfPeaks,
                scanCentroidResult,
                c_double(0),
                massList,peakFlags,arsize
                )
            
            
        data = array(massList.value)
        return data[0], data[1]    
    
    def get_ScanHeaderInfoForScanNum(self, scan_number):
        
        nScanNumber = c_long(scan_number) # get info for the twelfth scan
        nPackets = c_long(0)
        dRetantionTime = c_double(0.0)
        dLowMass = c_double(0.0)
        dHighMass = c_double(0.0)
        dTIC = c_double(0.0)
        dBasePeakMass = c_double(0.0)
        dBasePeakIntensity = c_double(0.0)
        nChannels =  c_long(0)
        bUniformTime = c_long(False)
        dFrequency = c_double(0.0)
        self.thermo_Library.GetScanHeaderInfoForScanNum(nScanNumber, 
                                                                nPackets, dRetantionTime,
                                                                dLowMass,
                                                                dHighMass, dTIC,
                                                                dBasePeakMass,
                                                                dBasePeakIntensity,
                                                                nChannels,
                                                                bUniformTime,
                                                                dFrequency)
        
       
        return dRetantionTime.value, dTIC.value 
    
    def get_mass_spectrums(self, file_name):
        
        Each_Mass_Spectrum = namedtuple('each_mass_spectrum', ['mass_list', 'abundance_list', 'retention_time', 'scan_number', 'tic_number'])
        
        if self.check_load_sucess():
            
            '''get number of scans'''
            nScans = self.get_scans_numbers()
            
            
            if nScans > 0: 
                
                list_Tics = list();
                
                list_RetentionTimeSeconds = list()
                
                '''key = scan_number or retention time'''
                
                for scan in range(1,nScans.value+1):
                        
                    '''get TIC and RT for each scan'''
                
                    #print self.get_A_B_ValueFromScanNum(scan)
                    retentionTimeSeconds, TIC  = self.get_ScanHeaderInfoForScanNum(scan)
                    
                    list_RetentionTimeSeconds.append(retentionTimeSeconds)
                    
                    list_Tics.append(TIC)
                    
                    #list_masses, list_Intensities = self.get_segment_mass_list_from_scan_num(scan)
                    
                
                
                    
                    mz, magnitude, resolution, base_noise, noise, charge = self.get_label_data(scan)
                    
                    self.get_centroid_peaks_nominal_mass(mz, magnitude, resolution, base_noise, noise, charge, self.list_of_tuples_mass_and_windows, file_name, scan, self.dict_result)
                    #ist_masses, list_Intensities = self.get_mass_list_from_scan_num(scan, 200, 2000)
                    #list_Intensities = (list_Intensities/max(list_Intensities))*100
                    #each_mass_spectrum = Each_Mass_Spectrum(mass_list=list_masses,
                    #                                        abundance_list=list_Intensities,
                    #                                        retention_time = retentionTimeSeconds,
                    #                                        scan_number = scan,
                    #                                        tic_number = list_Tics[0])
                    
                #return each_mass_spectrum, list_Tics, array(list_RetentionTimeSeconds)
            
            else:
            
                self.break_it = True
                #return None, None, None   
                
        else:
            pass
            #self.break_it = True
            #return None, None, None   
    def get_centroid_peaks_nominal_mass(self, massa, intes, resolution, base_noise, noise, charge, list_of_tuples_mass_and_windows, file_name, scan, dict_result):    
        
        massa_centr = massa
        intes_centr = intes
        
        dict_nominal = {}
        print len(massa_centr)
        print len(intes_centr)
        print len(resolution)
        print len(base_noise)
        print len(charge)
                
        for mz_index in range(len(massa_centr)):
            
            mz_nominal = int(massa_centr[mz_index])
            
            if dict_nominal.has_key(mz_nominal):
                #if intes_centr[mz_index] > 0.1:
                    dict_nominal.get(mz_nominal)[0].append(massa_centr[mz_index])
                    dict_nominal.get(mz_nominal)[1].append(intes_centr[mz_index]) 
                    dict_nominal.get(mz_nominal)[2].append(resolution[mz_index])
                    dict_nominal.get(mz_nominal)[3].append(base_noise[mz_index]) 
                    dict_nominal.get(mz_nominal)[4].append(noise[mz_index]) 
                    dict_nominal.get(mz_nominal)[5].append(charge[mz_index])
                
            else:
               
                dict_nominal[mz_nominal] = [[massa_centr[mz_index]],[intes_centr[mz_index]],[resolution[mz_index]],[base_noise[mz_index]],[noise[mz_index]],[charge[mz_index]]] 
            
        for tuple_mass_window in list_of_tuples_mass_and_windows:
            
            mass_referencia = tuple_mass_window[0]
            window_error = tuple_mass_window[1]
            
            abundance_thresould = tuple_mass_window[2]
            
            abundance_thresould_method = tuple_mass_window[3]
            abundance_thresould_method = ''.join(abundance_thresould_method.split())
            
            mz_reference_nominal = int(tuple_mass_window[0])
            
            if abundance_thresould_method == "%R.A.":
                print abundance_thresould_method
            
            
            mz_reference_nominal_plus1 =  mz_reference_nominal + 1
            mz_reference_nominal_minus1 =  mz_reference_nominal - 1
             
            if dict_nominal.has_key(mz_reference_nominal):
                
                
                for index in range(len(dict_nominal.get(mz_reference_nominal)[0])):
                    
                    cada_mz = dict_nominal.get(mz_reference_nominal)[0][index]
                    cada_intensity = dict_nominal.get(mz_reference_nominal)[1][index]
                    base_noise = dict_nominal.get(mz_reference_nominal)[3][index]
                    noise = dict_nominal.get(mz_reference_nominal)[4][index]
                    error = mass_referencia - cada_mz
                    
                    if -window_error <= error <=  window_error:
                        
                        if abundance_thresould_method == "%R.A.":
                            
                            cada_intensity = cada_intensity
                        else:
                            
                            cada_intensity = (cada_intensity - base_noise)/noise
                        
                        if cada_intensity > abundance_thresould:        
                            
                            if dict_result.has_key(mass_referencia):
                                
                                dict_result[mass_referencia].append((dict_nominal.get(mz_reference_nominal)[0][index], #massa
                                                             dict_nominal.get(mz_reference_nominal)[1][index], #intes
                                                            dict_nominal.get(mz_reference_nominal)[2][index], #resolution
                                                            dict_nominal.get(mz_reference_nominal)[3][index], #base_noise
                                                            dict_nominal.get(mz_reference_nominal)[4][index], #noise
                                                            dict_nominal.get(mz_reference_nominal)[5][index], #charge
                                                            scan,
                                                            file_name))
                            else:
                                
                                    
                                dict_result[mass_referencia] = [(dict_nominal.get(mz_reference_nominal)[0][index], #massa
                                                             dict_nominal.get(mz_reference_nominal)[1][index], #intes
                                                            dict_nominal.get(mz_reference_nominal)[2][index], #resolution
                                                            dict_nominal.get(mz_reference_nominal)[3][index], #base_noise
                                                            dict_nominal.get(mz_reference_nominal)[4][index], #noise
                                                            dict_nominal.get(mz_reference_nominal)[5][index], #charge
                                                            scan,
                                                            file_name)]
           
            if dict_nominal.has_key(mz_reference_nominal_plus1):
                
                
                for index in range(len(dict_nominal.get(mz_reference_nominal_plus1)[0])):
                    
                    cada_mz = dict_nominal.get(mz_reference_nominal_plus1)[0][index]
                    cada_intensity = dict_nominal.get(mz_reference_nominal_plus1)[1][index]
                    base_noise = dict_nominal.get(mz_reference_nominal_plus1)[3][index]
                    noise = dict_nominal.get(mz_reference_nominal_plus1)[4][index]
                    error = mass_referencia - cada_mz
                    
                    if -window_error <= error <=  window_error:
                        
                        if abundance_thresould_method == "%R.A.":
                            
                            cada_intensity = cada_intensity
                        else:
                            
                            cada_intensity = (cada_intensity - base_noise)/noise
                        
                        if cada_intensity > abundance_thresould:        
                            
                            if dict_result.has_key(mass_referencia):
                                
                                dict_result[mass_referencia].append((dict_nominal.get(mz_reference_nominal_plus1)[0][index], #massa
                                                             dict_nominal.get(mz_reference_nominal_plus1)[1][index], #intes
                                                            dict_nominal.get(mz_reference_nominal_plus1)[2][index], #resolution
                                                            dict_nominal.get(mz_reference_nominal_plus1)[3][index], #base_noise
                                                            dict_nominal.get(mz_reference_nominal_plus1)[4][index], #noise
                                                            dict_nominal.get(mz_reference_nominal_plus1)[5][index], #charge
                                                            scan,
                                                            file_name))
                            else:
                                
                                    
                                dict_result[mass_referencia] = [(dict_nominal.get(mz_reference_nominal_plus1)[0][index], #massa
                                                             dict_nominal.get(mz_reference_nominal_plus1)[1][index], #intes
                                                            dict_nominal.get(mz_reference_nominal_plus1)[2][index], #resolution
                                                            dict_nominal.get(mz_reference_nominal_plus1)[3][index], #base_noise
                                                            dict_nominal.get(mz_reference_nominal_plus1)[4][index], #noise
                                                            dict_nominal.get(mz_reference_nominal_plus1)[5][index], #charge
                                                            scan,
                                                            file_name)]
            
            if dict_nominal.has_key(mz_reference_nominal_minus1):
                
                
                for index in range(len(dict_nominal.get(mz_reference_nominal_minus1)[0])):
                    
                    cada_mz = dict_nominal.get(mz_reference_nominal_minus1)[0][index]
                    cada_intensity = dict_nominal.get(mz_reference_nominal_minus1)[1][index]
                    base_noise = dict_nominal.get(mz_reference_nominal_minus1)[3][index]
                    noise = dict_nominal.get(mz_reference_nominal_minus1)[4][index]
                    error = mass_referencia - cada_mz
                    
                    if -window_error <= error <=  window_error:
                        
                        if abundance_thresould_method == "%R.A.":
                            
                            cada_intensity = cada_intensity
                        else:
                            
                            cada_intensity = (cada_intensity - base_noise)/noise
                        
                        if cada_intensity > abundance_thresould:        
                            
                            if dict_result.has_key(mass_referencia):
                                
                                dict_result[mass_referencia].append((dict_nominal.get(mz_reference_nominal_minus1)[0][index], #massa
                                                             dict_nominal.get(mz_reference_nominal_minus1)[1][index], #intes
                                                            dict_nominal.get(mz_reference_nominal_minus1)[2][index], #resolution
                                                            dict_nominal.get(mz_reference_nominal_minus1)[3][index], #base_noise
                                                            dict_nominal.get(mz_reference_nominal_minus1)[4][index], #noise
                                                            dict_nominal.get(mz_reference_nominal_minus1)[5][index], #charge
                                                            scan,
                                                            file_name))
                            else:
                                
                                    
                                dict_result[mass_referencia] = [(dict_nominal.get(mz_reference_nominal_minus1)[0][index], #massa
                                                             dict_nominal.get(mz_reference_nominal_minus1)[1][index], #intes
                                                            dict_nominal.get(mz_reference_nominal_minus1)[2][index], #resolution
                                                            dict_nominal.get(mz_reference_nominal_minus1)[3][index], #base_noise
                                                            dict_nominal.get(mz_reference_nominal_minus1)[4][index], #noise
                                                            dict_nominal.get(mz_reference_nominal_minus1)[5][index], #charge
                                                            scan,
                                                            file_name)]
       