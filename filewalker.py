import os
import hashlib
import progress

def collectPaths(basePath):
    filepaths = []
    for base, dirs, files in os.walk(basePath):
        for name in files:
            filepaths.append(os.path.join(base, name))
    return filepaths

def calculateHash(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                hasher.update(block)    
    except PermissionError as e:
        print("Could not process", filepath, ":", e)
    return hasher.hexdigest()

def calculateHashes(filespaths):
    fileInfos = []
    total = len(filespaths)
    i = 0
    for filepath in filespaths:
        i += 1
        progress.progress(i, total, "Calculating Hashes")
        fileInfos.append({"filepath":filepath,"digest":calculateHash(filepath)})
    return fileInfos
