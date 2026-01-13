import option_importer
import os
import hashlib
import shutil

# Get file hashes to check for changes
def getFileHash(filePath) -> str:
    #print(f"Calculating hash for file: {filePath}")
    hasher = hashlib.sha256()
    with open(filePath, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# Explore the directory tree of a given folder
def walkGivenFilePath(filepath) -> dict:
    #print(f"Walking through file path: {filepath}")
    file_dict = dict()
    for dirpath, dirname, filenames in os.walk(filepath):
        if filenames == []:
            file_dict[""] = "No files found in this directory."
        for filename in filenames:
            individual_file = os.path.join(dirpath, filename)
            file_hash = getFileHash(individual_file)
            file_dict[individual_file] = file_hash
    
    return file_dict

# Compare what differences are there between the source folder and the destination folder
def compareSourceAndDestination(source, destination) -> tuple:
    print(f"Comparing source: {source} with destination: {destination}")
    source_dict = walkGivenFilePath(source)
    dest_dict = walkGivenFilePath(destination)
    source_keys = source_dict.keys()
    dest_values = dest_dict.values()

    differing_files = []

    for key in source_keys:
        if key != "":
            if source_dict[key] not in dest_values:
                relative_destination = os.path.relpath(key, source)
                differing_files.append((key, destination + "\\" + relative_destination))

    return differing_files

# Import settings and start the copy process
if __name__ == "__main__":
    
    print("Starting Folder Sync Tool...")
    source_array, destination_array = option_importer.finalizeOptionsImport()
    for i in range(len(destination_array)):
        source = source_array[i]
        destination = destination_array[i]
        print(f"Syncing from source: {source} to destination: {destination}")
        differing_files = compareSourceAndDestination(source, destination)
        amount = len(differing_files)

        if differing_files == []:
            print(f"No different file hashes were found.\nALL FILES ARE SYNCED")
        else:
            errors = 0
            errors_array = []
            for file in differing_files:
                try:
                    print(f"Copying file: {file[0]}")
                    source_file, dest_file = file
                    if not os.path.exists(os.path.dirname(dest_file)):
                        os.makedirs(os.path.dirname(dest_file))
                    shutil.copy2(source_file, dest_file)
                except:
                    print(f'AN ERROR OCCURED DURING THE SYNC PROCESS ! - {file[0]} was not copid successfully  !')
                    errors += 1
                    errors_array.append(file[0])

            print(f"\nCoppied {amount-errors}/{amount} files successfully !")
            if errors_array != []:
                print("\nThese files were not successfully copied over:")
                for _ in errors_array:
                    print(_)

