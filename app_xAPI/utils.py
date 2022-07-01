"""
simple functions to help with file management
"""
import time

def newjson(folderpath, content):
    """
    write a new json file filled with content in folderpath 
    using current the time as its name
    """
    filename = str(time.time_ns())
    f = open(folderpath+"/"+filename, "w")
    f.write(content)
    f.close()
