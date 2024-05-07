import csv

colors = ["green", "green", "red", "yellow"]

filename = "button_colors.csv"

try:
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(colors)
    print("CSV file with colors created successfully:", filename)
except Exception as e:
    print("Error creating CSV file:", e)