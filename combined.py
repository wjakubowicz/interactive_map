import pandas as pd
from geopy.exc import GeocoderServiceError
from geopy.geocoders import ArcGIS
import time
import csv
import folium
from folium.plugins import FastMarkerCluster

input_file = 'spis.csv'
output_file = 'spis_with_coordinates.csv'
output_map = 'map.html'

latitudes = []
longitudes = []
records = []

def get_coordinates(address):
    geolocator = ArcGIS()
    try:
        location = geolocator.geocode(address)
        if location is None:
            return (None, None)  # or raise an exception
        return (location.latitude, location.longitude)
    except GeocoderServiceError:
        time.sleep(1)  # delay for 1 second
        return get_coordinates(address)  # try again

df = pd.read_csv(input_file, delimiter=';')  # Read the CSV file

# Iterate over addresses and get coordinates
for address in df['Adres:']:
    if pd.isna(address) or address == "nan":
        latitudes.append(None)
        longitudes.append(None)
    else:
        lat, lon = get_coordinates(address)
        latitudes.append(lat)
        longitudes.append(lon)
        print(f"Address: {address}, Latitude: {lat}, Longitude: {lon}")

# Add latitude and longitude as new columns to the DataFrame
df['Latitude'] = latitudes
df['Longitude'] = longitudes

# Save the modified DataFrame back to a CSV file
df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
print("Updated CSV file saved as " + output_file + ".")

with open(output_file, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    keys = [key.strip() for key in reader.fieldnames]
    for row in reader:
        record = {key.strip(): row[key.strip()] for key in keys}
        records.append(record)

map = folium.Map(location=[52.114503, 19.423561], zoom_start=7, tiles='CartoDB dark_matter') # Change the location and zoom level to focus on Poland

marker_cluster = FastMarkerCluster(data=[])  # Initialize FastMarkerCluster

# Iterate through each row to add markers with popups
for record in records:
    if record['Latitude'] and record['Longitude']:
        try:
            # Prepare location
            location = [float(record['Latitude']), float(record['Longitude'])]
            # Dynamically extracting all the information to include in the popup
            popup_text = ""
            for key, value in record.items():
                popup_text += f"<b>{key}:</b> {value}<br>"
            
            popup = folium.Popup(popup_text, max_width=450)
            
            # Create the marker
            marker = folium.Marker(
                location=location,
                popup=popup
            )
            
            # Add the marker to the FastMarkerCluster instead of directly to the map
            marker_cluster.add_child(marker)
            
        except ValueError as e:
            print(f"Error converting to float for record: {record}. Error: {e}")

map.add_child(marker_cluster)  # Add FastMarkerCluster to the map after all markers have been added to it

map.save(output_map)  # Save the map