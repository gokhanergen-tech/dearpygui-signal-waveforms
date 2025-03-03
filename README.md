# Signal Visualiser

### Author: Gökhan Ergen  
**Programming Language:** Python  
**Used Tools:**
- **dearpygui** (For GUI Application)
- **scipy** (For sawtooth visualization)
- **numpy** (For mathematical calculations)

---

## Parameters:

- **A: Amplitude**
  - Controls the amplitude of the waves.

- **DC: Direct Current Offset**
  - A constant value that offsets the waveform vertically.

- **FI0: Initial Phase**
  - Phase shift value.

- **Fs: Sampling Frequency**
  - Indicates how many samples are collected per second.

- **Fsig: Frequency Signal**
  - Determines the cycle count of signals. A cycle takes `1/Fsig` seconds.  
  - Example: If `Fsig = 0.2Hz`, then the cycle count is `5` seconds.

---

## Application Features

In this application, you can visualize sampled **sinusoidal**, **square**, and **sawtooth** waveforms using the above parameters. The time range of signals is calculated as:
  
`(max_time - min_time) * Fs`
  
because `Fs` represents the sampling frequency per second. The program provides a simple GUI to adjust parameters dynamically.

### **Sinusoidal Wave**
- Default waveform is **sinusoidal**.
- Signal time range: `0 to 10`
- Formula: `A * sin(2π * Fsig * t + FI0) + DC`
- Example: If `A = 4` and `DC = 1`, then:
  - Maximum positive value: `5`
  - Minimum negative value: `-3`

### **Square Wave**
- The square wave signal follows this rule:
  - `signal_wave = sin(2π * Fsig * t)`
  - If `signal_wave >= 0`: output is `1`
  - Otherwise: output is `-1`

### **Sawtooth Wave**
- Uses **scipy** library for visualization.
- Follows the same parameter set as other waveforms.

### **Example Use Case**
Changing the time range to `-100 to 100` will display a sinusoidal waveform over this range.

If `Fsig` is changed to `0.5 Hz`, the period `T` is calculated as:

`T = 1 / 0.5 = 2s`

---

## **Dependencies and Installation**

### **Python Version:**
- Python `3.11.5`

### **Required Libraries:**
- `scipy: 1.11.3`
- `numpy: 1.26.0`
- `dearpygui: 1.9.0`

### **Installation:**
```bash
pip install numpy scipy dearpygui
```

### **Run the Application:**
```bash
python signal_visualiser.py
```

---

## **License**
This project is for educational purposes.

---

## **Author**
Developed by **Gökhan Ergen**

