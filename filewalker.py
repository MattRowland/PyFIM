import os
import hashlib
import progress

def collect_paths(basePath):
    print("Walking path...")
    filepaths = []
    for base, dirs, files in os.walk(basePath):
        for name in files:
            filepaths.append(os.path.join(base, name))
    return filepaths

def calculate_hash(filepath):
    print("Calculating hashes...")
    hasher = hashlib.sha256()
    print()
    try:
        with open(filepath, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                hasher.update(block)    
    except PermissionError as e:
        print("Could not process", filepath, ":", e)
    return hasher.hexdigest()

def calculate_hashes(filespaths):
    fileInfos = []
    total = len(filespaths)
    i = 0
    for filepath in filespaths:
        i += 1
        progress.progress(i, total, "Calculating Hashes")
        fileInfos.append({"filepath":filepath,"digest":calculate_hash(filepath)})
    return fileInfos

def detect_duplicates(fileInfos):
    dictionary = {}
    for fileInfo in fileInfos:
        print(fileInfo)
        if fileInfo["digest"] in dictionary:
            dictionary[fileInfo["digest"]].append(fileInfo["filepath"])
        else:
            dictionary[fileInfo["digest"]] = [fileInfo["filepath"]]

    duplicateItems = []
    for digest, filepaths in dictionary.items():
        if len(filepaths) > 1:
            duplicateItems.append({"digest":digest, "filepaths":filepaths})

    if len(duplicateItems) == 0:
        print("No Duplicates!")
    else:
        print("Duplicate Items")
        for item in duplicateItems:
            print("-"*74)
            print("--- ",item["digest"].upper()," ---")
            print("\n".join(item["filepaths"]))
            print("-"*74)