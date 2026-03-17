from datetime import datetime
import json
import os

priority_weight = {
    "low": 1,
    "average": 2,
    "high": 3
}

entry_list = []


def show_menu():
    print("PLANNER")
    print("1. Load file")
    print("2. New entry")
    print("3. Show entries")
    print("4. Edit entry")
    print("5. Save to file")
    print("0. Close the program")
#creating the entry
def create_entry():
    print("CREATING NEW ENTRY")
    #subject / "What?"
    while True: 

        subject = input("Subject *: ").strip() #removing blank characters, so space or enter won't be accepted as entry subject
        if subject: #check if empty/blank
            break
        else:
            print("This section can't be empty. Try again.")
    #date and time / "When?"
    while True: 

        date_time = input("Time and date (DD.MM.YYYY HH:MM) *: ").strip()
        try:
            dt = datetime.strptime(date_time, "%d.%m.%Y %H:%M")
            date_time = dt.strftime("%d.%m.%Y %H:%M")
            break
        except ValueError:
            print("Wrong input. Use DD.MM.YYYY HH:MM.")
    #localisation / "Where?"
    localisation = input("Localisation: ").strip() 
    #priority / "Is important?"
    while True: 
        priority = input("What priority does this event have? Choose low, average or high: ").strip().lower()
        if priority == "":
            priority = "low"
            break
        elif priority in ["low", "average", "high"]:
            break
        else:
            print("Invalid choice. Choose low, average or high.")
    #description / "What is this about?"
    while True: 
        description = input("Description (max. 256 characters): ").strip()
        if len(description) <= 256:
            break
        else:
            print("Maximum length exceeded. Please re-enter the description.")

    new_entry = {
        "subject": subject,
        "date_time": date_time,
        "localisation": localisation,
        "priority": priority,
        "description": description
    }

    entry_list.append(new_entry)
    print("New entry added.")

#viewing existing entries
def view_entries(entry_list):
    global priority_weight
    if not entry_list: 
        print("No entries found.")
        return
    print("\nSort entries\n1. First created (default)\n2. Date and time (by oldest) \n3. Date and time (by newest)\n4. Priority")
    sort_type = input("Select: ").strip()

    if sort_type == "2":
        entry_list.sort(key=lambda entry: datetime.strptime(entry["time"], "%d.%m.%Y %H:%M"))
    elif sort_type == "3":
        entry_list.sort(reverse=True, key=lambda entry: datetime.strptime(entry["time"], "%d.%m.%Y %H:%M"))
    elif sort_type == "4":
        entry_list.sort(reverse=True, key=lambda entry: priority_weight.get(entry["priority"], 0))
    else:
        print("ENTRIES")
    for entry_index, entry in enumerate(entry_list, start=1):
        print(f"\nEntry #{entry_index}:")
        print(f"Subject: {entry['subject']}")
        print(f"Date and time: {entry['date_time']}")
        print(f"Localisation: {entry['localisation']}")
        print(f"Priority: {entry['priority']}")
        print(f"Description: {entry['description']}")
    
#editing entries
def edit_entry(entry_list):
    if not entry_list:
        print("No entries available.")
        return

    print("EDIT ENTRY")
    for entry_index, entry in enumerate(entry_list, start=1):
        print(f"{entry_index}. {entry['subject']} ({entry['date_time']})")

    while True:
        try:
            choice = int(input("Select which entry to edit: "))
            if 1 <= choice <= len(entry_list):
                selected_entry = entry_list[choice-1]
                break
            else:
                print("Invalid number.")
        except ValueError:
            print("Enter number.")

    print("\nSelected entry:")
    for entry_key, value in selected_entry.items():
        print(f"{entry_key.capitalize()}: {value}")

    decision = input("Do you want to edit or delete the entry? Type edit or delete: ").strip().lower()
    if decision == "delete":
        confirm = input("Are you sure? ").strip().lower()
        if confirm == "yes":
            entry_list.pop(choice-1)
            print("Entry deleted.")
        else:
            print("Operation cancelled.")
    elif decision == "edit":
        # edit form
        print("Press Enter to leave the current contents.")
        subject = input(f"Subject [{selected_entry['subject']}]: ").strip()
        if subject:
            selected_entry['subject'] = subject

        while True:
            date_time = input(f"Date and time [{selected_entry['time']}] (DD.MM.YYYY HH:MM): ").strip()
            if not date_time:
                break
            try:
                dt = datetime.strptime(date_time, "%d.%m.%Y %H:%M")
                selected_entry['time'] = dt.strftime("%d.%m.%Y %H:%M")
                break
            except ValueError:
                print("Invalid input.")

        localisation = input(f"localisation [{selected_entry['localisation']}]: ").strip()
        if localisation:
            selected_entry['localisation'] = localisation

        while True:
            priority = input(f"priority [{selected_entry['priority']}] (low/average/high): ").strip().lower()
            if not priority:
                break
            if priority in ["low", "average", "high"]:
                selected_entry['priority'] = priority
                break
            else:
                print("Invalid input.")

        while True:
            description = input(f"description [{selected_entry['description']}]: ").strip()
            if not description:
                break
            if len(description) <= 256:
                selected_entry['description'] = description
                break
            else:
                print("Max. lenght: 256 char.")

        print("Entry updated.")
    else:
        print("Invalid input. Returning to menu")

#saving to file
save_file = "day_plan.json"
def save_to_file(entry_list):

    print("SAVING TO FILE")
    select_file = input(f"Save to default file '{save_file}'? ").strip().lower()
    if select_file == "No":
        file_name = input("Type file name: ").strip()
        if not file_name.endswith(".json"):
            file_name += ".json"
    else:
        file_name = save_file

    try:
        with open(file_name,"w", encoding="utf-8") as save:
            json.dump(entry_list, save, ensure_ascii=False, indent=4)
        print(f"Saved as '{file_name}'.")
    except Exception as error:
        print(f"An error occured while trying to save: {error}")
   
#reading the file
def read_file():
    print("READING THE FILE")
    files = [file for file in os.listdir() if file.endswith(".json")]
    if not files:
        print("No available files with .json extention in this localisation.")
        return None
    
    print("Available files: ")
    for file_index, file in enumerate(files, start=1):
        print(f"{file_index}.{file}")

    while True:
            select_file = input("Select file to upload or type " + "Cancel" + " to cancel: ").strip().lower()

            if select_file == "cancel":
                print("Uploading cancelled.")
                return None
            try:
                select_file = int(select_file)
                if 1 <= select_file <= len(files):
                    selected_file = files[select_file-1]
                    break
                else:
                    print("Invalid input. Try again.")
            except ValueError:
                print("Invalid input. Type a number.")

    try:
        with open(selected_file, "r", encoding="utf-8") as file:
            list = json.load(file)
        print(f"Uploaded the data from '{selected_file}'.")
        return list
    except Exception as error:
        print(f"An error occured while trying to read the file: {error}")
        return None


while True:
    show_menu()

    try:
        choice = int(input("Select option:  "))
    except ValueError:
        print("Try again. Select from options below: ")
        continue

    if choice == 1:
        new_entries = read_file()
        if new_entries is not None:
            entry_list = new_entries
        else:
            print("The previous entries were not cleared.")
    elif choice == 2:
        create_entry()
    elif choice == 3:
        view_entries(entry_list)
    elif choice == 4:
        edit_entry(entry_list)
    elif choice == 5:
        save_to_file(entry_list)
    elif choice == 0:
        if_save = input("Do you want to save before closing the program?").strip().lower()
        if if_save == "yes":
            save_to_file(entry_list)
        else:
            print("See you soon!")
            break
    else:
        print("Invalid input, try again.")
