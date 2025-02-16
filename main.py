import dearpygui.dearpygui as dpg
import numpy as np

from frequence_options import FrequencyOptions, wave_forms


frequency_options = FrequencyOptions()

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

def render_signal():
    dpg.delete_item(viewer_signal_parent_tag,children_only=True)
    with dpg.plot(label="Stem Plot Example", height=-1, width=-1, parent=viewer_signal_parent_tag):
                dpg.add_plot_axis(dpg.mvXAxis, label="X Axis", tag="x_axis")
                dpg.add_plot_axis(dpg.mvYAxis, label="Y Axis", tag="y_axis")
                
                x, y = frequency_options.calculate_signals()
                dpg.add_stem_series(x,y, label="Signal", parent="y_axis",tag="stem_graph")
                

def update_stem_graph():
    x, y = frequency_options.calculate_signals()
    dpg.set_value("stem_graph",[x,y])
                

def handle_change_wave_form(_, value):
    if value!=frequency_options.wave_form:
     setattr(frequency_options, "wave_form", value)
     update_stem_graph()

def handle_change_values(s, d, a):
   setattr(frequency_options, a, d)
   update_stem_graph()
    
def main():
    dpg.create_context()

    with dpg.window(tag="Primary Window") as window:
        dpg.add_text("Generate Signals")
        with dpg.drawlist(width=1280, height=2):
             dpg.draw_line((0, 0), (1280, 0), color=(150, 150, 150, 64), thickness=0.5)
        with dpg.group(horizontal=True):
         with dpg.group():
       
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
