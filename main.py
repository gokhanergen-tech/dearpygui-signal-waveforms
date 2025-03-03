import dearpygui.dearpygui as dpg
import numpy as np

from difference_sinusoidal_options import DifferenceSinusoidal
from frequence_options import FrequencyOptions, wave_forms


frequency_options = FrequencyOptions()
difference_sinusoidals = DifferenceSinusoidal()

input_fields = [
        ("Ampitute", "ampitute"),
        ("DC", "dc"),
        ("FI0", "fi0"),
        ("FSIG", "f_sig_hz"),
        ("FS", "fs_hz"),
        ("Min Time", "min_time"),
        ("Max Time", "max_time")
    ]

viewer_signal_parent_tag = "signal_viewer"

graph_types = [
    "Waveforms",
    "Difference Sinusoidal Signals"
]

signal_process_types = [
    "default","mean","rms","var","std","median","immediate_power","average_power","energy"
]



global graph_type
graph_type = None

def render_signal():
    dpg.delete_item(viewer_signal_parent_tag,children_only=True)
    with dpg.plot(label="Stem Plot Example", height=-1, width=-1, parent=viewer_signal_parent_tag):
                dpg.add_plot_axis(dpg.mvXAxis, label="X Axis", tag="x_axis")
                dpg.add_plot_axis(dpg.mvYAxis, label="Y Axis", tag="y_axis")
                dpg.add_stem_series([],[], label="Signal", parent="y_axis",tag="stem_graph")
                
                update_stem_graph()
       

def render_difference_sinusoidal_type(x,y,analyzed_data):
       dpg.add_line_series(x,y, label="Signal", parent="y_axis",tag="line_graph")
       ipower = analyzed_data["ipower"]
       dpg.add_line_series(x, ipower,parent="y_axis",tag="ipower")
       dpg.add_stem_series(x, ipower,parent="y_axis",tag="ipower_stem")
       
       dpg.set_axis_limits("y_axis",np.min(y), np.max(ipower))  
     
         
       data = [
    ("Mean value", analyzed_data["average"], "V"),
    ("RMS value", analyzed_data["rmse"], "V"),
    ("Variance", analyzed_data["variance"], "V^2"),
    ("Standard deviation", analyzed_data["std"], "V"),
    ("Median", analyzed_data["median"], "V"),
    ("Mean power", analyzed_data["average_power"], "V^2"),
    ("Energy", analyzed_data["energy"], "J")
]   
       dpg.delete_item("table_analysis")
       with dpg.table(header_row=True, 
                       borders_innerH=True, 
                       borders_outerH=True, 
                       borders_innerV=True, 
                       borders_outerV=True, 
                       parent="difference_signals",
                       tag="table_analysis"):
        
         dpg.add_table_column(label=" ")
         dpg.add_table_column(label="Own algorithm")
         dpg.add_table_column(label="Unit")
         for row in data:
          with dpg.table_row():
                for item in row:
                    dpg.add_text(item)
           

def update_stem_graph():
    x, y, analyzed_data = graph_type == "Waveforms" and frequency_options.calculate_signals() or difference_sinusoidals.calculate_signals()
    if x is None or y is None:
        return
    dpg.set_value("stem_graph",[x,y])
    dpg.set_axis_limits("x_axis",np.min(x), np.max(x))
    dpg.set_axis_limits("y_axis",np.min(y), np.max(y))  
    dpg.delete_item("line_graph")
    dpg.delete_item("ipower")
    dpg.delete_item("ipower_stem")
    
    if(graph_type != "Waveforms"):
       render_difference_sinusoidal_type(x,y,analyzed_data)
        
    

def handle_change_wave_form(_, value):
    if value!=frequency_options.wave_form:
     setattr(frequency_options, "wave_form", value)
    update_stem_graph()
    
def handle_change_values(s, d, a):
   setattr(graph_type == "Waveforms" and frequency_options or difference_sinusoidals, a, d)
   update_stem_graph()
     
def handle_change_graph_type(_, value):
    global graph_type
    
    if graph_type == value:
        return
    
    dpg.delete_item("settings",children_only=True)
    graph_type = value
    if value == "Waveforms":
        with dpg.group(parent="settings"):
          for label, attr in input_fields:
            common_params = {
               "label":label,
               "default_value":getattr(frequency_options, attr),
               "callback":handle_change_values,
               "width":1280/(len(input_fields)+4),
               "user_data":attr
               
           }
            dpg.add_spacer(height=10)
            if(attr in ["fs_hz", "max_time","min_time"]):
             dpg.add_input_int(
             **common_params)
            else:
             dpg.add_input_float(
             **common_params,
             step=attr=="fi0" and np.pi/8 or 0.1,
            
           )
          dpg.add_combo(items=wave_forms,
                      callback=handle_change_wave_form,
                      default_value=frequency_options.wave_form,
                      label="Waveform", width=100)
          dpg.add_spacer(height=100)
    else:
        with dpg.group(parent="settings",tag="difference_signals", width=300):
            dpg.add_input_int(label="fs1 hz", default_value=difference_sinusoidals.f1s, callback=handle_change_values, user_data="f1s")            
            dpg.add_input_int(label="fs2 hz", default_value=difference_sinusoidals.f2s, callback=handle_change_values, user_data="f2s")      
            dpg.add_input_int(label="fs hz", default_value=difference_sinusoidals.fs, callback=handle_change_values, user_data="fs")  
            dpg.add_input_int(label="N samples", default_value=difference_sinusoidals.N, callback=handle_change_values, user_data="N") 
    
    
    if dpg.does_item_exist("stem_graph"):
     update_stem_graph()
        


def main():
    dpg.create_context()

    with dpg.window(tag="Primary Window") as window:
        dpg.add_text("Generate Signals")
        with dpg.drawlist(width=1280, height=2):
             dpg.draw_line((0, 0), (1280, 0), color=(150, 150, 150, 64), thickness=0.5)
        dpg.add_combo(items=graph_types,
                      callback=handle_change_graph_type,
                      default_value="Waveforms",
                      label="Examples", width=100)
        with dpg.group(horizontal=True):
         with dpg.group(tag="settings"):
           handle_change_graph_type(None, "Waveforms")
         with dpg.child_window(height=-25, tag=viewer_signal_parent_tag):
              render_signal()
        dpg.add_text("Gökhan ERGEN - Signal Visuliser")
            

      
    dpg.create_viewport(title='Generate Signals', width=1280, height=640, x_pos=0, y_pos=0)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
    
if __name__ == "__main__":
    main()
