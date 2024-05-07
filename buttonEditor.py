import csv

class ButtonEditor:
    def __init__(self, filename=None):
        if filename is not None:
            self.filename = filename
        self.button_colors = [None, None, None, None]  # Initialize button colors
        
    def saveColors(self, colors):
        for i, color in enumerate(colors):
            self.set_button_color(i,color)
        self.save_csv_file

    def set_button_color(self, button_index, color):
        if button_index < 0 or button_index >= 4:
            raise ValueError("Button index out of range")
        self.button_colors[button_index] = color
    
    def get_button_color(self, button_index):
        if button_index < 0 or button_index >= 4:
            raise ValueError("Button index out of range")
        return self.button_colors[button_index]
    
    def get_button_colors(self):
        """
        Get the colors of all buttons.
        """
        return self.button_colors

    def read_csv_file(self, filename):
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.reader(file)
                for row_index, row in enumerate(reader):
                    if row_index >= 4:
                        break  # Stop reading if more than 4 rows
                    for col_index, color in enumerate(row):
                        if col_index >= 4:
                            break  # Stop reading if more than 4 columns
                        self.set_button_color(col_index, color)
        except FileNotFoundError:
            print("File not found")
    
    def save_csv_file(self, filename, button_colors):
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(button_colors)
            print("CSV file with colors created successfully:", filename)
        except Exception as e:
            print("Error creating CSV file:", e)
'''
# Example usage:
button_writer = ButtonWriter("button_colors.csv")
button_writer.read_csv_file()
print("Button colors from file:", button_writer.button_colors)

# Set new colors
button_writer.set_button_color(0, "Red")
button_writer.set_button_color(1, "Green")
button_writer.set_button_color(2, "Blue")
button_writer.set_button_color(3, "Yellow")

# Save new colors to file
button_writer.save_csv_file()
print("New button colors saved to file")
'''