import dearpygui.dearpygui as dpg
import numpy as np

class SnrSinusoidal:
    __snr_value = 10
    __sinusoidal_instance = None
    
    def __init__(self, sinusoidal_instance):
         self.__sinusoidal_instance = sinusoidal_instance
         
    @property
    def snr_value(self):
        return self.__snr_value
    
    @snr_value.setter
    def snr_value(self, value):
        self.__snr_value = value
        self.calculate_snr_series()
        
    def calculate_snr_series(self):
        (x,y, _) = self.__sinusoidal_instance.calculate_signals()
        u_rmse_signal = np.sqrt((self.__sinusoidal_instance.dc**2)+((self.__sinusoidal_instance.ampitute**2)/2))
        u_rmse_noise = u_rmse_signal/(10**(self.__snr_value/20))
        noise_signal = np.random.normal(0, u_rmse_noise, len(x))
        superimposed_noise = y+noise_signal
        hist, bin_edges = np.histogram(noise_signal, bins=64)
        
        dpg.set_value("snr_sinusoidal", [x,y])
        dpg.set_value("snr_sinusoidal_noise", [x,noise_signal])
        dpg.set_value("snr_noise_hist",[bin_edges.tolist(),hist.tolist()])
        dpg.set_value("snr_noise_super_imposed", [x,superimposed_noise.tolist()])
        dpg.configure_item("noise_signal_plot",label = f"Signal and noisy separately shown (desired SNR: {self.__snr_value})")
    
    def render(self, parent):
        
        with dpg.group(parent=parent):
            dpg.add_input_int(label="SNR", 
                              min_clamped=True, 
                              min_value=10, step=1, 
                              default_value=self.__snr_value, 
                              callback=lambda _,value:setattr(self, "snr_value",value))
            
            with dpg.group(horizontal=True, width=500):
             with dpg.plot(tag="noise_signal_plot"):
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="x_axis_snr")
                        dpg.add_plot_axis(dpg.mvYAxis, label="Voltage (V)", tag="y_axis_snr")
                        dpg.add_line_series([],[], label="Signal", parent="y_axis_snr",tag="snr_sinusoidal")
                        dpg.add_line_series([],[], label="Noise", parent="y_axis_snr",tag="snr_sinusoidal_noise")
                         
             with dpg.plot(label="Frequency distribution histogram"):
                        dpg.add_plot_axis(dpg.mvXAxis, label="Voltage (V)", tag="x_axis_snr_noise_hist")
                        dpg.add_plot_axis(dpg.mvYAxis, label="Frequency (-)", tag="y_axis_snr_noise_hist")
                        dpg.add_bar_series([],[], label="", parent="y_axis_snr_noise_hist",tag="snr_noise_hist")
            
             with dpg.plot(label=""):
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="x_axis_snr_super_imposed_noise")
                        dpg.add_plot_axis(dpg.mvYAxis, label="Voltage (V)", tag="y_axis_snr_super_imposed_noise")
                        dpg.add_line_series([],[], label="Superimposed noise", parent="y_axis_snr_super_imposed_noise",tag="snr_noise_super_imposed")
                 
        self.calculate_snr_series()
                

        