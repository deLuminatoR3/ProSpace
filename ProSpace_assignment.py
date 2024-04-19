import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

#Define Parameters
global num_samples, min_voltage, max_voltage, noise_level, error
num_samples = 10
min_voltage = 0.0
max_voltage = 5.0
noise_level = 0.1
percentage_error = 5

updated_voltage = []

#Function to generate new data and diplay it 
def generate_data_and_display():
    
    #Generate random voltage with some noise
    global updated_voltage    
    voltage = np.random.uniform(min_voltage, max_voltage, num_samples)
    #voltage = (max_voltage - min_voltage) * np.random.rand(num_samples) + min_voltage
    #voltage = np.random.normal((max_voltage - min_voltage)/2, 1, num_samples)
    noise = np.random.normal(0, noise_level, num_samples)    
    voltage += noise
    
    #Update the voltage values by ignoring existing values 
    updated_voltage = list(voltage)
    
    #Calculate Analysis metrics
    mean_voltage = np.mean(voltage)
    std_dev_voltage = np.std(voltage)
    voltage_range = np.ptp(voltage)
    e = voltage_range * percentage_error / 100
    faulty_nozzles = np.where((voltage <= min_voltage+e) | (voltage >= max_voltage-e))[0]
    
    #Update the Analysis metrics onto the GUI interface 
    label_mean.config(text=f"Mean Voltage: {mean_voltage:.2f}")
    label_std_dev.config(text=f"Standard Deviation: {std_dev_voltage:.2f}")
    label_range.config(text=f"Voltage Range: {voltage_range:.2f}")
    label_faulty_nozzles.config(text=f"Faulty Nozzles Indices: {faulty_nozzles}")
    
    #Clear all previous plots
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()
    fig.suptitle('Sensor Data Analysis')
    
    #Ploting all plots again
    faulty_index =  set(faulty_nozzles)
    for i, v in enumerate(voltage):
        if i in faulty_index:
            axs[0].plot(i, v, 'r.')
        else:
            axs[0].plot(i, v, 'b.')
    axs[0].plot(voltage)
    axs[0].axhline(mean_voltage, color='black', linestyle='-', label='Mean')
    axs[0].axhline(min_voltage + e, color='b', linestyle='--', label='Faulty Line')
    axs[0].axhline(max_voltage - e, color='b', linestyle='--')
    axs[0].legend(loc='upper right', fontsize='small')
    axs[0].set_xlabel('Number of Sample')
    axs[0].set_ylabel('Voltage')
    
    faulty_voltages_count = len(faulty_index)
    non_faulty_voltages_count = len(voltage) - faulty_voltages_count
    sizes = [non_faulty_voltages_count, faulty_voltages_count]
    labels = ['Non-faulty', 'Faulty']
    axs[1].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    
    axs[2].hist(voltage, int(len(voltage)/3))
    axs[2].set_xlabel('Voltage')
    axs[2].set_ylabel('Frequency')
    axs[2].axvline(mean_voltage, color='r', linestyle='-', label='Mean')
    axs[2].axvline(mean_voltage - std_dev_voltage, color='b', linestyle='--', label='Std. Deviation')
    axs[2].axvline(mean_voltage + std_dev_voltage, color='b', linestyle='--')
    axs[2].legend(loc = 'upper right', fontsize='small')
    
    canvas.draw()

#Function to generate new data, add it to the existing data and diplay it
def update_data_and_display():
    
    #Generate random voltage with some noise
    global updated_voltage    
    voltage = np.random.uniform(min_voltage, max_voltage, num_samples)
    noise = np.random.normal(0, noise_level, num_samples)    
    voltage += noise
    
    #Upadate the existing voltage values
    updated_voltage.extend(list(voltage))
    
    mean_voltage = np.mean(updated_voltage)
    std_dev_voltage = np.std(updated_voltage)
    voltage_range = np.ptp(updated_voltage)
    e = voltage_range * percentage_error / 100
    faulty_nozzles = np.where((updated_voltage <= min_voltage+e) | (updated_voltage >= max_voltage-e))[0]
    
    label_mean.config(text=f"Mean Voltage: {mean_voltage:.2f}")
    label_std_dev.config(text=f"Standard Deviation: {std_dev_voltage:.2f}")
    label_range.config(text=f"Voltage Range: {voltage_range:.2f}")
    label_faulty_nozzles.config(text=f"Faulty Nozzles Indices: {faulty_nozzles}")
    
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()    
    fig.suptitle('Sensor Data Analysis')
    
    faulty_index =  set(faulty_nozzles)
    for i, v in enumerate(updated_voltage):
        if i in faulty_index:
            axs[0].plot(i, v, 'r.')
        else:
            axs[0].plot(i, v, 'b.')
    axs[0].plot(updated_voltage)
    axs[0].axhline(mean_voltage, color='black', linestyle='-', label='Mean')
    axs[0].axhline(min_voltage + e, color='b', linestyle='--', label='Faulty Line')
    axs[0].axhline(max_voltage - e, color='b', linestyle='--')
    axs[0].legend(loc='upper right', fontsize='small')
    axs[0].set_xlabel('Number of Sample')
    axs[0].set_ylabel('Voltage')
    
    faulty_voltages_count = len(faulty_index)
    non_faulty_voltages_count = len(updated_voltage) - faulty_voltages_count
    sizes = [non_faulty_voltages_count, faulty_voltages_count]
    labels = ['Non-faulty', 'Faulty']
    axs[1].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    
    axs[2].hist(updated_voltage, int(len(updated_voltage)/3))
    axs[2].set_xlabel('Voltage')
    axs[2].set_ylabel('Frequency')
    axs[2].axvline(mean_voltage, color='r', linestyle='-', label='Mean')
    axs[2].axvline(mean_voltage - std_dev_voltage, color='b', linestyle='--', label='Std. Deviation')
    axs[2].axvline(mean_voltage + std_dev_voltage, color='b', linestyle='--')
    axs[2].legend(loc = 'upper right', fontsize='small')
    
    canvas.draw()

#Create tkinter window
root = tk.Tk()
root.title("ProSpace: Sensor Data Generatation and Analysis")

#Setup layouts for GUI
label1 = tk.Label(root, 
                 text=f"Initial Parameters taken:",
                 font=('Helvetica 11 bold') ,justify='left', padx=25)
label1.grid(row=0, column=0, columnspan=3, sticky='w')
label2 = tk.Label(root, 
                 text=f"num_samples = {num_samples}\nmin_voltage = {min_voltage}\nmax_voltage = {max_voltage}\nnoise_level = {noise_level}\n\nThe following data is created using the random module from numpy. The Faulty values are calculated by considering a safety factor of {percentage_error}% in the voltages.",
                 font=('Helvetica 11') ,justify='left', padx=25)
label2.grid(row=1, column=0, columnspan=3, sticky='w')

#Creating frame to display the Analysis results
frame = tk.LabelFrame(root, text='Data Analysis', padx=5, pady=5)
frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

#Pushing the Plots and Analysis metrics to the frame
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12,4))
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=0, columnspan=3)

label_mean = tk.Label(frame, text="", font=('Helvetica 10 bold'))
label_std_dev = tk.Label(frame, text="", font=('Helvetica 10 bold'))
label_range = tk.Label(frame, text="", font=('Helvetica 10 bold'))
label_faulty_nozzles = tk.Label(frame, text="", font=('Helvetica 10 bold'))

label_mean.grid(row=1, column=0)
label_std_dev.grid(row=1, column=1)
label_range.grid(row=1, column=2)
label_faulty_nozzles.grid(row=2, column=0, columnspan=3)

#Creating buttons for exiting the program, generating and updating data
button_exit = tk.Button(root, text="Exit Program", command=root.quit, padx=50, pady=10)
button_generate_data = tk.Button(root, text='Generate Data', command=generate_data_and_display, padx=50, pady=10)
button_update_data = tk.Button(root, text='Update Data', command=update_data_and_display, padx=50, pady=10)

button_exit.grid(row=3, column=0, padx=5, pady=5)
button_generate_data.grid(row=3, column=1, padx=5, pady=5)
button_update_data.grid(row=3, column=2, padx=5, pady=5)

#Generate and Display the initial data
generate_data_and_display()

#tkinter event loop
root.mainloop()
