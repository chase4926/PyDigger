#!/usr/bin/env python

"""
Generates the file ores.yaml in YAML format. Obviously.

This list comes from the wikipedia page "Abundance of elements in Earth's crust"
The list should provide more element information than is necessary for any game.

----
Adapted from kmonsoor's answer on:
http://stackoverflow.com/questions/11790535/extracting-data-from-html-table

----
To install the libraries to run this file:
pip install beautifulsoup4
pip install PyYAML
"""

import urllib2
import yaml
from bs4 import BeautifulSoup
from lib_misc import getRandomColor


HTML_FILE = 'elements-cached.html'

def write_html_file(html):
  with open(HTML_FILE, 'w+') as f:
    f.write(html)

def read_html_file():
  with open(HTML_FILE, 'r') as f:
    return f.read()

try:
  # Open the URL
  response = urllib2.urlopen('https://en.wikipedia.org/wiki/Abundance_of_elements_in_Earth%27s_crust')
  # Write updated version of file
  write_html_file(response.read())
except urllib2.URLError:
  print "Could not open url!"
  print "Cached version will be used."

# Read the html into Soup
soup = BeautifulSoup(read_html_file(), "html.parser")

# Grab the table html
table = soup.find("table")

# Walk through the table compiling a list of the items
datasets = []
for row in table.find_all("tr")[1:]:
  dataset = []
  for td in row.find_all("td"):
    dataset.append(td.get_text())
  datasets.append(dataset)

# Convert list into yaml file and only take the parts that are useful
yaml_dict = {}

for element in datasets:
  y_dict = {}
  y_dict['z'] = int(str(element[1]).replace(',', ''))
  if element[5] == '':
    element[5] = 0
  y_dict['amount'] = float(str(element[5]).replace(',', ''))
  y_dict['color'] = getRandomColor()
  yaml_dict[str(element[2])] = y_dict


# Function for the below sorting
def sort_by_z(key):
  return yaml_dict[key]['z']

z_sorted = sorted(yaml_dict, key=sort_by_z, reverse=False)

# Convert Z to game-usable z levels
last_z = yaml_dict[z_sorted[0]]['z']
level = 10
for key in z_sorted:
  z = yaml_dict[key]['z']
  if z != last_z:
    level += 5
  yaml_dict[key]['z'] = level


with open('ores2.yaml', 'w+') as f:
  for key in z_sorted:
    f.write(yaml.dump({key: yaml_dict[key]}))
  #f.write(yaml.dump(yaml_dict))

