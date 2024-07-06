# Geocoding and Mapping Script

This Python script is designed to read addresses from a CSV file, geocode these addresses to obtain latitude and longitude coordinates, and then generate an interactive map with markers for each address. The script utilizes the `pandas` library for data manipulation, `geopy` for geocoding addresses, and `folium` for creating the interactive map.

## Features

- **Geocoding**: Converts addresses into geographic coordinates (latitude and longitude) using the ArcGIS geocoding service.
- **Data Enrichment**: Adds latitude and longitude as new columns to the original CSV file.
- **Interactive Map Generation**: Creates an HTML file displaying a map with markers for each geocoded address. Each marker includes a popup with detailed information.

## Requirements

Before running this script, ensure you have the following Python libraries installed:

- pandas
- geopy
- folium

You can install these libraries using pip:

```bash
pip install pandas geopy folium
```

## Usage

1. Prepare your CSV file with addresses. The script expects a column named `Adres:` containing the addresses to be geocoded.
2. Update the [`input_file`] variable in the script to point to your CSV file.
3. Run the script:

```bash
python combined.py
```

4. The script will generate two files:
   - An updated CSV file (`spis_with_coordinates.csv`) with added columns for latitude and longitude.
   - An HTML file (`map.html`) containing the interactive map.

## Input File Format

The input CSV file should be formatted with a delimiter of `;` and include at least one column named `Adres:` containing the addresses.

Example:

```csv
Adres:
123 Example St, City, Country
456 Another Rd, City, Country
```

## Output

- **CSV File**: The output CSV file will include the original data plus two new columns for latitude (`Latitude`) and longitude (`Longitude`).
- **Interactive Map**: The HTML file will display a dark-themed map with markers for each address. Clicking on a marker will show a popup with all the information from the CSV file for that address.

## Customization

You can customize the script by modifying the input and output file names, changing the map's initial location and zoom level, or by adjusting the popup information format.

## Note

The script includes error handling for geocoding service errors and invalid addresses. It will retry once if a geocoding service error occurs and skip addresses that cannot be geocoded.
```