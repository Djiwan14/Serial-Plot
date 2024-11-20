import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re

# Replace 'COM5' with your actual Arduino's port
SERIAL_PORT = 'COM5'  # Change to the correct port
BAUD_RATE = 9600

# Initialize serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Allow time for the connection to establish
ser.reset_input_buffer()  # Clear buffer before starting

# Data containers for plotting
temperature_data = []
humidity_data = []
time_data = []

# Start time to track elapsed time
start_time = time.time()

# Regular expression to match valid data lines (e.g., "30.00 39.00;")
data_pattern = re.compile(r"^(-?\d+\.\d+)\s(-?\d+\.\d+);$")

def read_serial_data():
    """Read and parse serial data from Arduino."""
    try:
        # Read a line from the serial buffer if available
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(f"Received raw data: {line}")  # Debugging: Print raw data

            # Match line to expected format
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

        # Keep only the most recent 100 data points for smoother visualization
        max_points = 100
        if len(time_data) > max_points:
            temperature_data.pop(0)
            humidity_data.pop(0)
            time_data.pop(0)

    # Plot temperature
    plt.subplot(2, 1, 1)
    plt.cla()  # Clear the subplot
    plt.plot(time_data, temperature_data, label="Temperature (°C)", color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (°C)')
    if len(temperature_data) > 0:
        plt.ylim(min(temperature_data) - 2, max(temperature_data) + 2)  # Dynamic y-axis
    plt.legend(loc='upper right')

    # Plot humidity
    plt.subplot(2, 1, 2)
    plt.cla()  # Clear the subplot
    plt.plot(time_data, humidity_data, label="Humidity (%)", color='blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Humidity (%)')
    if len(humidity_data) > 0:
        plt.ylim(min(humidity_data) - 2, max(humidity_data) + 2)  # Dynamic y-axis
    plt.legend(loc='upper right')

    plt.tight_layout()

# Set up the figure for live plotting
plt.figure(figsize=(10, 6))

ani = FuncAnimation(plt.gcf(), update_plot, interval=500, cache_frame_data=False)

plt.tight_layout()
plt.show()

ser.close()
