import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import threading

def close_plot():
    time.sleep(1)
    plt.close()

# Pfad zu deiner .nc-Datei
file_path = '<füge hier den richtigen Pfad ein>/HWD_EU_climate_rcp45_stdev_v1.0.nc'

# Öffne die NetCDF-Datei
dataset = nc.Dataset(file_path)

# Anzeigen der Metadaten
print(dataset)

# Anzeigen der Variablen in der Datei
print(dataset.variables.keys())

# Extrahiere die Zeitvariable
time_var = dataset.variables['time']
time_units = time_var.units
time_data = nc.num2date(time_var[:], units=time_units)

# Anzeigen der Zeitdaten
#print(time_data)

# Erstelle einen einfachen Plot
for year in range(1986, 2086):

# Starte einen Thread, um das Plot-Fenster nach 5 Sekunden zu schließen
    thread = threading.Thread(target=close_plot)
    thread.start()

#for year in range(1986, 2051):
# Beispiel: Filtern nach einer bestimmten Zeit
    desired_time = datetime(year, 1, 1, 0)  # Beispiel: 1. Januar 2050, 00:00 Uhr
    time_index = np.where(time_data == desired_time)[0][0]

    print(year)

# Extrahiere die Daten für die gewünschte Zeit
    variable_name = 'HWD'  # Ersetze dies durch den tatsächlichen Variablennamen in deiner Datei
    data = dataset.variables['HWD_EU_climate'][time_index, :, :]
    lat = dataset.variables['lat'][:]
    lon = dataset.variables['lon'][:]

# Zeichnen einer 2D-Karte der Daten für die gewünschte Zeit
    plt.figure(figsize=(12, 6))
    plt.contourf(lon, lat, data)  # Zeit ist bereits ausgewählt
    plt.colorbar(label=f'{variable_name} (units)')  # Ersetze 'units' durch die tatsächliche Einheit der Variable
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'{variable_name} Distribution on {desired_time}')
    plt.show()
