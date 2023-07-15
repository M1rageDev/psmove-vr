import os

def save(file, text):
    with open(file, "w") as f:
        f.write(text)

def read(file):
    with open(file, "r") as f:
        data = f.read()
    return data

def doIfNotExists(file):
    return not os.path.isfile(file)
