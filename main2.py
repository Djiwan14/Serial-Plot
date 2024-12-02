import serial
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


SERIAL_PORT = 'COM5'
BAUD_RATE = 9600
LOG_FILE = "inhaler_data_log.csv"

def parse_received_data(data_line, measurement_time):
    """
    Parse received data and format it as required.
    """
    try:
        parts = data_line.strip().split()
        if len(parts) != 2:
            return None

        temperature = float(parts[0])
        humidity = float(parts[1].strip(';'))


        now = datetime.now()
        year, month, day = now.year, now.month, now.day
        hour, minute, second = now.hour, now.minute, now.second


        atmospheric_pressure = 950.0
        pressure_drop = round(1.0 / (measurement_time + 1), 2)  # Simulated

        return {
            "Year": year,
            "Month": month,
            "Day": day,
            "Hour": hour,
            "Minute": minute,
            "Second": second,
            "Temperature (C)": temperature,
            "Humidity (%)": humidity,
            "Atmospheric Pressure (hPa)": atmospheric_pressure,
            "Measurement Time (s)": round(measurement_time, 2),
            "Pressure Drop (kPa)": pressure_drop
        }
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None

def save_data_to_csv(data, file_name):
    """
    Save data to a CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}")

def plot_data(data):
    """
    Visualize the inhalation data.
    """
    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))

    # Plot pressure drop over time
    plt.plot(df['Measurement Time (s)'], df['Pressure Drop (kPa)'], label='Pressure Drop (kPa)')
    plt.xlabel('Measurement Time (s)')
    plt.ylabel('Pressure Drop (kPa)')
    plt.title('Inhalation Data: Pressure Drop Over Time')
    plt.legend()
    plt.grid()
    plt.show()

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"Failed to connect to {SERIAL_PORT}: {e}")
        return

    inhalation_data = []
    measurement_time = 0.0

    try:
        while True:
            line = ser.readline().decode('utf-8')
            if line:
                print(f"Received: {line.strip()}")
                parsed_data = parse_received_data(line, measurement_time)
                if parsed_data:
                    inhalation_data.append(parsed_data)
                    measurement_time += 0.14  # Increment measurement time
    except KeyboardInterrupt:
        print("Data collection stopped by user.")
    finally:
        ser.close()
        print("Serial connection closed.")

        if inhalation_data:
            save_data_to_csv(inhalation_data, LOG_FILE)
            plot_data(inhalation_data)

if __name__ == "__main__":
    main()
