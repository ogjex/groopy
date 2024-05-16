from person_editor import PersonEditor
from person import Person

def main():
    # Create a PersonEditor instance
    editor = PersonEditor()


    # Save sample Person objects to CSV file
    editor.save_csv(filename='sample_persons.csv')

if __name__ == "__main__":
    main()