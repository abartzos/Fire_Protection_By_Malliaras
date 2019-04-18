import csv
import random
import pickle 
from multiDKNN import MultiDKNN

"Baseline and +-value"
baseline_temp = 20.0
baseline_humid = 68.0
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


# loads the data and converts it to num
fires_str = load_csv('forestfires.csv')
fires = []

for i in fires_str:
    fires.append([float(i[0]), float(i[1])])

feature_names = ['temperature', 'humidity']
normal = []

"""Generates not-fire data"""

for i in range(len(fires)):
    normal.append([baseline_temp+random.randint(-temp_range,temp_range),
    baseline_humid+random.randint(-humid_range,humid_range)])

# creates labels
fire_labels = ["fire" for i in range(len(fires))]
normal_labels = ["not_fire" for i in range(len(normal))]

y = fire_labels + normal_labels
x = fires + normal

clf = MultiDKNN()
clf.fit(x,y)

filehandler = open('classifier', 'wb')
pickle.dump(clf, filehandler)