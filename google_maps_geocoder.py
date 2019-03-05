"""
When dealing with bulk CSV uploads for routes, there are two ways to upload them. (1) Using addresses
that are saved in the address book on the Samsara dashboard or by (2) using the full address, latitude,
and longitude.  With the second option, its likely you do not have the gps coordinates for an address.
This script allows you to input a list of addresses via csv and output a new csv with address, latitude,
and longitude.
"""

import requests
import json
import csv

# Place your Google Maps API Key here as a string
API_KEY = ''

"""
CSV File Format - List addresses in first column of Excel

	Col 1
-------------
| Address 1 |
-------------
| Address 2 |
-------------
| Address 3 |
-------------

Address , City , State Abv & Zip Code
Example: 444 De Haro St, San Francisco, CA 94107
"""

# The 'read_csv_addresses' function takes in the csv file with address as an argument.
# The function reads the addresses, puts them into a list, and returns that list of addresses.

def read_csv_addresses(input_file):

	with open(input_file) as csvfile:

	    readCSV = csv.reader(csvfile)

	    # creates empty list
	    address_list = []

	    # populates that empty list with addresses from csv file
	    for row in readCSV:
	        addr = row[0]
	        address_list.append(addr)

	return address_list


# The 'geocode_address_to_gps_coordinates' function takes in a list of addresses as an argument. 
# The function formats the url, makes the request to the Google Maps API, and extracts lat/lng values.
# The function returns a dictionary with the three keys: Address, Latitude, and Longitude. The
# coresponding values are gathered in list with as many addresses included in the input file.
def geocode_address_to_gps_coordinates(address_list):

	# creates dictionary to store address, latitude, and
	address_dict = {'Address': [] , 'Latitude': [], 'Longitude': []}
	
	count = 0

	for addr in address_list:
		
		formatted_addr = addr.replace(' ','+')

		geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}{}{}".format(formatted_addr,'&key=',API_KEY)

		# Makes call to Google Maps API and converts results to JSON format:
		results = requests.get(geocode_url)
		results = results.json()

		latitude_temp = results['results'][0]['geometry']['location']['lat']
		longitude_temp = results['results'][0]['geometry']['location']['lng']

		address_dict['Address'].append(addr)
		address_dict['Latitude'].append(latitude_temp)
		address_dict['Longitude'].append(longitude_temp)
		
		# Makes the duration of waiting for this script to run more visually pleasing.
		count = count + 1
		if count == 20:
			print('This may take some time if there are a lot of addresses. Please wait...')
	
	return address_dict

# The 'create_output_csv' function takes in a dictionary with the format returned by the
# 'geocode_address_to_gps_coordinates' function as an argument. The function creates a new 
# csv file, titled 'gps_coordinates.csv'. Format of the output csv is as follows:
"""
	Col 1         Col 2          Col 3
------------ -------------- ----------------
| Address 1 |  Latitude 1  |  Longitude 1  |
------------ -------------- ----------------
| Address 2 |  Latitude 2  |  Longitude 2  |
------------ -------------- ----------------
| Address 3 |  Latitude 3  |  Longitude 3  |
------------ -------------- ----------------
"""

def create_output_csv(address_dict):

	with open('gps_coordinates.csv', mode='w') as csv_file:
		output_csv = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		address_count = len(address_dict['Address'])

		for index in range(address_count):
	
			addr = address_dict['Address'][index] 
			lat = address_dict['Latitude'][index] 
			lng = address_dict['Longitude'][index] 
			output_csv.writerow([addr, lat, lng])


# The csv file with address being uploaded must be in the same folder as this script.
csv_file = input("Please enter name of csv file with full addresses: \n> ")

# Calls 'read_csv_address' function to gather addresses from cvs file and put them in a list.
list_of_addresses = read_csv_addresses(csv_file)

# Google Map API is called and dictionary with pertinent information is created.
gps_coordinates = geocode_address_to_gps_coordinates(list_of_addresses)

# New cvs file is created
create_output_csv(gps_coordinates)
print('Complete. New output cvs file,"gps_coordinates.csv" has been created!')
