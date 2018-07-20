
import Constantes
from numpy import array, sqrt, mean, float64

class UsefulFunctions()

   def calc_kendrick(self, exact_mass):
        
        km = (14/14.01565)*exact_mass
        
        nominal_km = round(km, 0)
        
        #for ICR
        kmd = (nominal_km - km) * 1000
        #kmd = (nominal_km - km) * 1
        
        return nominal_km, km, round(kmd,0)
        
   def calc_kendrick_array(self, exact_mass_array):
        
        exact_mass = np.array([round(i,5) for i in exact_mass_array])
        
        Hmass = Constantes.atomic_masses.get('H')
        
        km = (14.00000/(12.00000+ (2*Hmass)))*exact_mass
        
        nominal_km = np.array([int(i) for i in km])
        #for ICR
        nominal_mass = np.array([int(i) for i in exact_mass])
        
        kmd = (nominal_mass - km) * 1000
        
        #kmd = (nominal_km - km) * 1
        
        kdm_array = np.array([round(i,0) for i in kmd])
        
        return nominal_km, km, kdm_array
   
   def ScaleAbundances(self, intensidades_list):
        #'0 to 100' 
        intensidades_array = np.array(intensidades_list)
        total = sum(intensidades)
               
        return ((intensidades_array * 100) / total)
   
   def get_erro_ppm(self, list_exp, list_teorico):
        
        one_M = 1000000
        vetor_exp  = array(list_exp)
        vetor_theo = array(list_teorico)
        
        return ((vetor_teorico-vetor_exp)/vetor_teorico)*one_M 
   
   def get_rms_error(self, error_list, round_to):
        
        return round(sqrt(mean(array(error_list)**2)), round_to)
        
    def get_mw_distribution(self, massa, intensidade):
        
        mass_intensidade = 0
        mass_squared_intensidade = 0
        for i in range(len(massa)):
            mass_intensidade = mass_intensidade + (massa[i]*intensidade[i])
            mass_squared_intensidade = mass_squared_intensidade + ((massa[i]**2)*(intensidade[i]))
        
        if mass_intensidade > 0:
            mw = mass_squared_intensidade/mass_intensidade
        else:
            mw = "NaN"
        return mw 
    
    def get_number_average_distribution_(self, max_mass, min_mass, massa, intensidade):
                
        mass_intensidade = 0
        for i in range(len(massa)):

            if  min_mass <= massa[i] <= max_mass:
                mass_intensidade = mass_intensidade + (massa[i]*intensidade[i])

        mw = mass_intensidade/sum(intensidade)

        return mw
        
   
