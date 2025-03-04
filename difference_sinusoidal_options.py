import math
import numpy as np
from functools import reduce


def mean_own(y):
    return math.fsum(y) / len(y)

def rmse_own(y):
    squared = [value**2 for value in y]
    return math.sqrt(math.fsum(squared) / len(y))

def variance_own(y, mean):
    difference_square = [(value-mean)**2 for value in y]
    
    return math.fsum(difference_square) / len(y)

def median_own(y):
    sorted_value = sorted(y)
    length = len(sorted_value)
    center_index = length//2
    if(length%2==1):
        return sorted_value[center_index]
    else:
        value = sorted_value[center_index]
        value_before = sorted_value[center_index-1]
        return (value+value_before)/2
    
    

class DifferenceSinusoidal:
    def __init__(self):
        self.__f1s = 2
        self.__f2s = 8
        self.__fs = 200
        self.__N = 100
        
    @property
    def f1s(self):
        return self.__f1s
    
    @f1s.setter
    def f1s(self, value):
        self.__f1s = value

    @property
    def f2s(self):
        return self.__f2s
    
    @f2s.setter
    def f2s(self, value):
        self.__f2s = value

    @property
    def fs(self):
        return self.__fs
    
    @fs.setter
    def fs(self, value):
        self.__fs = value

    @property
    def N(self):
        return self.__N
    
    @N.setter
    def N(self, value):
        self.__N = value

        
    def calculate_signals(self):
        if not self.N or not self.fs or not self.f1s or not self.f2s:
            return (None, None, None)
            
        min_step = 0
        Ts = 1/self.__fs
        x = range(min_step, self.N)
    
        y = [(5*np.cos(2*np.pi*self.__f1s*k*Ts)-2*np.sin(2*np.pi*self.__f2s*k*Ts)) for k in x]
        
        power = np.power(y,2)
        energy = np.sum(power)
        rmse = np.sqrt(energy/self.N)
        average = np.mean(y)
        variance = (1/self.N)*np.sum(np.power((y-average),2))
        std = np.sqrt(variance)
        median = np.median(y)
        
        own_mean = mean_own(y)
        own_rmse = rmse_own(y)
        own_variance = variance_own(y, own_mean)
        own_std = math.sqrt(own_variance)
        own_median = median_own(y)
        own_average_power = own_rmse**2
        own_energy = own_average_power*len(y)
        
        
        
        
        analyzed_data={
            "rmse":"{:.4f}".format(rmse),
            "variance":"{:.4f}".format(variance),
            "std":"{:.4f}".format(std),
            "median":"{:.4e}".format(median),
            "average":"{:.4e}".format(average),
            "ipower":power,
            "own_rmse":"{:.4f}".format(own_rmse),
            "own_average_power":"{:.4f}".format(own_average_power),
            "own_median":"{:.4e}".format(own_median),
            "own_std":"{:.4f}".format(own_std),
            "own_variance":"{:.4f}".format(own_variance),
            "own_rmse":"{:.4f}".format(own_rmse),
            "own_average":"{:.4e}".format(own_mean),
            "own_energy":round(own_energy)
            
        }
      
        return ([i/self.__fs for i in x],y,analyzed_data)
        
    
