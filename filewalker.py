import os
import hashlib

def collectPaths(basePath):
    filepaths = []
    for base, dirs, files in os.walk(basePath):
        for name in files:
            filepaths.append(os.path.join(base, name))
    return filepaths

def calculateHash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            hasher.update(block)
    return hasher.hexdigest()

def calculateHashes(filespaths):
    fileInfos = []
    for filepath in filespaths:
        fileInfos.append({"filepath":filepath,"digest":calculateHash(filepath)})
    return fileInfos
