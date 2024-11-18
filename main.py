import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


SERIAL_PORT = 'COM5'
BAUD_RATE = 9600


ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Give time to establish connection


temperature_data = []
humidity_data = []
time_data = []


start_time = time.time()

def read_serial_data():
    """Read and parse serial data from Arduino."""
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line.endswith(";"):
            try:
                temp, hum = map(float, line[:-1].split())
                return temp, hum
            except ValueError:
                print(f"Invalid data received: {line}")
                return None, None
    return None, None

def update_plot(frame):
    """Update the plot with new data."""
    temp, hum = read_serial_data()
    if temp is not None and hum is not None:
        elapsed_time = time.time() - start_time
        temperature_data.append(temp)
        humidity_data.append(hum)
        time_data.append(elapsed_time)

        plt.clf()

        # Plot temperature data
        plt.subplot(2, 1, 1)
        plt.plot(time_data, temperature_data, label="Temperature (°C)")
        plt.xlabel('Time (s)')
        plt.ylabel('Temperature (°C)')
        plt.ylim(min(temperature_data) - 2, max(temperature_data) + 2)  # Dynamic y-axis
        plt.legend(loc='upper right')

        # Plot humidity data
        plt.subplot(2, 1, 2)
        plt.plot(time_data, humidity_data, label="Humidity (%)", color='orange')
        plt.xlabel('Time (s)')
        plt.ylabel('Humidity (%)')
        plt.ylim(min(humidity_data) - 2, max(humidity_data) + 2)  # Dynamic y-axis
        plt.legend(loc='upper right')

        plt.tight_layout()


plt.figure(figsize=(10, 6))


ani = FuncAnimation(plt.gcf(), update_plot, interval=1000, cache_frame_data=False)

plt.tight_layout()
plt.show()

ser.close()
