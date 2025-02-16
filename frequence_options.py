from scipy import signal
import numpy as np


wave_forms = ["sinusoidal", "square", "saw_toothed"]


class FrequencyOptions:
    __ampitute = 2
    __dc = 1
    __fi0 = 0
    __f_sig_hz = 0.2
    __fs_hz = 5
    __wave_form = wave_forms[0]
    __max_time = 10
    __min_time = 0
    
    def __init__(self):
     """ Frequency Settings class
      Default Properties:
       ampitute = 2
       dc = 1
       fi0 = 0
       f_sig_hz = 0.2
       fs_hz = 5
       wave_form = sinusoidal
       max_time = 10
       min_time = 0
     """
    pass
    

    @property
    def ampitute(self):
        return self.__ampitute
    
    @property
    def dc(self):
        return self.__dc
    
    @property
    def fi0(self):
        return self.__fi0
    
    @property
    def f_sig_hz(self):
        return self.__f_sig_hz
    
    @property
    def fs_hz(self):
        return self.__fs_hz
    
    @property
    def max_time(self):
        return self.__max_time
    
    @property
    def min_time(self):
        return self.__min_time
    
    @property
    def wave_form(self):
        return self.__wave_form
    
    @ampitute.setter
    def ampitute(self, value):
        self.__ampitute = value
        
    @dc.setter
    def dc(self, value):
        self.__dc = value
        
    @fi0.setter
    def fi0(self, value):
        self.__fi0 = value
        
    @f_sig_hz.setter
    def f_sig_hz(self, value):
        self.__f_sig_hz = value
        
    @fs_hz.setter
    def fs_hz(self, value):
        self.__fs_hz = value
        
    @max_time.setter
    def max_time(self, value):
        self.__max_time = value
        
    @min_time.setter
    def min_time(self,value):
        self.__min_time = value
    
    @wave_form.setter
    def wave_form(self,value):
        self.__wave_form = value
        
    def calculate_signals(self):
        
        """
        Calculation Current Waveforms
        
        If you update the selected signal options, you can calculate x and y values to use.

        Returns:
            Tupple: (x, y)
        """
        
        x = np.linspace(self.min_time,self.__max_time,self.fs_hz*(self.__max_time-self.__min_time), endpoint=False)
    
        
        if self.wave_form != "saw_toothed":
         sinusoidal_signals = np.sin(x*2*np.pi*self.f_sig_hz+self.fi0)
         match self.wave_form:
            case "sinusoidal":
                y = self.ampitute*sinusoidal_signals+self.dc
            case "square":
                y = self.ampitute*np.where(sinusoidal_signals>=0,1,-1)+self.dc
        else:
          y = self.ampitute*signal.sawtooth(2 * np.pi * self.f_sig_hz * x)+self.dc
        

        return (x,y)