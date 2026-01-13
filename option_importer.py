
import os
import json
from string import digits

# Checks if we have created options file before
def checkIfOptionsExist():
    print("Checking if options file exists...")
    if os.path.exists("./options.foldertool"):
        return True
    return False

# Requests user for a index to remove from options.foldertool, itterates over all the dictionary entries put makes an exception for the index user provided and ignores it when creating a brand new options.foldertool
def removeOption():
    options = importOptionsFromFile()
    new_dict = {}
    ind_str = str(input(f"Available indexes:{(options)}\nWhich index would you like to remove? (numbers only) "))
    ind = int(ind_str)
    
    print(f"Your new dictionary:{new_dict}")
    # Why I said "brand new" is here we are "w"ing and not "a"ing.
    with open("./options.foldertool", "w") as f:
        for dictionary in options:
            x = 0
            for i in range(len(options)):
                if f'source{ind}' not in dictionary.keys():
                    new_dict[f'source{i}'] = dictionary[f'source{i}']
                    new_dict[f'dest{i}'] = dictionary[f'dest{i}']
                    

# Create settings file to store designated source and destination folders
def createOptions():
    # If the options.foldertool doesn't exist create it.
    if not checkIfOptionsExist():
        source = input("Enter source directory path: ")
        dest = input("Enter destination directory path: ")
        dictory = {
            f"source0": source,
            f"dest0": dest
        }

        with open("./options.foldertool", "a") as f:
            json.dump(dictory, f)
            f.write("\n============================\n")
    else :
        print("Options file already exists.")
        Options = importOptionsFromFile()
        if not Options:
            os.remove("./options.foldertool")
            print("Deleting empty options.foldertool file...")
            createOptions()
        latestOption = Options[-1]
        latestOptionKeys = list(latestOption.keys())
        print(f"Latest option index found: {latestOptionKeys[0]}")
        latestOptionIndex = ""
        for key in latestOption.keys():
            latestOptionIndex = str(latestOptionKeys[0]).replace("source", "")
            latestOptionIndex = int(latestOptionIndex)
            latestOptionIndex += 1
        
        checkIfUserWantsToAddMore = input("Do you want to add another option or remove an option? (y/n/r): ")
        if checkIfUserWantsToAddMore.lower() == "r":
            removeOption()
            createOptions()
        elif checkIfUserWantsToAddMore.lower() != "y":
            return
        source = input("Enter source directory path: ")
        dest = input("Enter destination directory path: ")
        dictory = {
            f"source{latestOptionIndex}": source,
            f"dest{latestOptionIndex}": dest
        }

        with open("./options.foldertool", "a") as f:
            json.dump(dictory, f)
            f.write("\n============================\n")

# Import the designated folder locations from options.foldertool file and convert them to Python dictionaries         
def importOptionsFromFile() -> list:
    print("Importing options from options.foldertool file...")
    dictionary_entries = []
    with open("./options.foldertool", "r") as f:
        optionsFile = f.read()
        for entry in optionsFile.split("\n============================\n"):
            if entry.strip() == "":
                continue
            data = json.loads(entry)
            dictionary_entries.append(data)

    return dictionary_entries

# Putting it all together...
def finalizeOptionsImport() -> tuple:
    print("Finalizing option imports...")
    source_entries = []
    dest_entries = []

    createOptions()
    options = importOptionsFromFile()
    latest_option = options[-1]
    for key in latest_option.keys():
        if "source" in key:
            source_entries.append(latest_option[key])
        elif "dest" in key:
            dest_entries.append(latest_option[key])
        
     
    return source_entries, dest_entries

