class MP_Worker(object):   
	
	def __init__(self, list_inputs1, list_inputs2):        
		    self.list_inputs1 = list_inputs1
	      self.list_inputs2 = list_inputs2 
    	
	def go(self):
    
        n_jobs = 8
        p = Pool(n_jobs) 
        results = p.map(self, [(input1, input2) for list_inputs1 , list_inputs2 in zip(self.list_inputs1, self.list_inputs2)])        
        p.close()       
        p.join()
        collect()
        return results
	
  def __call__(self, args):
		    return self.find_every_class(args[0],args[1])
   
  def worker_function(self, input1, input2):
        
        result = dosometing using input 1 , and 2                
		    return result 
