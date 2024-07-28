import sqlite3
import matplotlib.pyplot as plt
from cs50 import SQL

# Connect to the database
db = SQL("sqlite:///temp.db")
# Fetch data from the database (example query)

# Process the fetched data
# Assuming column1 is for x-axis

weights = [65, 50, 75]
excercises = ['chest', 'legs', 'arms']

def fudge():
    for i in range(len(weights)):
        curr_weight = weights[i]
        curr_ex = excercises[i]
        db.execute("INSERT INTO fake (weights, excercise) VALUES (?, ?)", curr_weight, curr_ex)


info = list(db.execute("select * from fake"))
exercise = [row[0] for row in data]

Assuming column2 is for y-axis
weight = [row[1] for row in data]


# Create a plot using Matplotlib
plt.figure(figsize=(8, 6))
bars = plt.bar(excercises, weights, color='blue')  # Bar chart

# Annotate each bar with its weight value
for bar, w in zip(bars, weights):
    plt.text(bar.get_x() + bar.get_width() / 2, w, str(w), ha='center', va='bottom')
plt.xlabel('exercise')
plt.ylabel('weight')
plt.title('Weight progression per exercise')
plt.xticks(rotation=45)
plt.grid(True)
plt.savefig("temp.png")
plt.show()
