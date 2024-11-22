import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re


SERIAL_PORT = 'COM5'
BAUD_RATE = 9600

# Initialize serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
ser.reset_input_buffer()


temperature_data = []
humidity_data = []
time_data = []


start_time = time.time()


data_pattern = re.compile(r"^(-?\d+\.\d+)\s(-?\d+\.\d+);$")

def read_serial_data():
    """Read and parse serial data from Arduino."""
    try:

        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received raw data: {line}")  # Debugging: Print raw data


            match = data_pattern.match(line)
            if match:
                temp = float(match.group(1))
                hum = float(match.group(2))
                print(f"Parsed data: Temperature={temp}, Humidity={hum}")  # Debugging
                return temp, hum
            else:
                print(f"Invalid data received: {line}")  # Debugging
    except Exception as e:
        print(f"Error reading data: {e}")

    return None, None

def update_plot(frame):
    """Update the plot with new data."""
    # Try reading data from the serial
    temp, hum = read_serial_data()

    if temp is not None and hum is not None:
        elapsed_time = time.time() - start_time
        temperature_data.append(temp)
        humidity_data.append(hum)
        time_data.append(elapsed_time)


        max_points = 100
        if len(time_data) > max_points:
            temperature_data.pop(0)
            humidity_data.pop(0)
            time_data.pop(0)


    plt.subplot(2, 1, 1)
    plt.cla()  # Clear the subplot
    plt.plot(time_data, temperature_data, label="Temperature (°C)", color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (°C)')
    if len(temperature_data) > 0:
        plt.ylim(min(temperature_data) - 2, max(temperature_data) + 2)  # Dynamic y-axis
    plt.legend(loc='upper right')


    plt.subplot(2, 1, 2)
    plt.cla()  # Clear the subplot
    plt.plot(time_data, humidity_data, label="Humidity (%)", color='blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Humidity (%)')
    if len(humidity_data) > 0:
        plt.ylim(min(humidity_data) - 2, max(humidity_data) + 2)  # Dynamic y-axis
    plt.legend(loc='upper right')

    plt.tight_layout()


plt.figure(figsize=(10, 6))

ani = FuncAnimation(plt.gcf(), update_plot, interval=500, cache_frame_data=False)

plt.tight_layout()
plt.show()

ser.close()
