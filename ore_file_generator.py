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

# Open the URL
response = urllib2.urlopen('https://en.wikipedia.org/wiki/Abundance_of_elements_in_Earth%27s_crust')

# Read the html into Soup
soup = BeautifulSoup(response.read())

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
  yaml_dict[str(element[2])] =y_dict

with open('ores2.yaml', 'w+') as f:
  f.write(yaml.dump(yaml_dict))
