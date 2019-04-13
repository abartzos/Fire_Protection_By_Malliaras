import csv
import random

"Baseline and +-value"
baseline_temp = 20.0
baseline_humid = 20.0
temp_range = 15.0
humid_range = 5.0


def load_csv(file_name):
    """
    imports a csv file as a list
    
    parameters: 
        file_name: string
    returns:
        reader: list
    """

    with open(file_name, 'r') as f:
        reader = csv.reader(f)
        return list(reader)


fires = load_csv('forestfires.csv')
feature_names = ['temperature', 'humidity']
normal = []

"""Generates not-fire data"""

for i in range(len(fires)):
    normal.append([baseline_temp+random.randint(-temp_range,temp_range),
    baseline_humid+random.randint(-humid_range,humid_range)])

fire_labels = ["fire" for i in range(len(fires))]

not_fire_labels = ["not_fire" for i in range(len(normal))]

