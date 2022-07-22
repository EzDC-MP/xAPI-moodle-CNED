"""
Simple functions to help with file management and accessing info in csv files.
"""
import time
import csv
import config
import os

def newjson(folderpath, content, filename=''):
    """
    write a new json file filled with content in folderpath 
    using current the time (in nanosecond) as its default name

    @requires folderpath a string of an existing folder path
    @param folderpath string of an existing folder path
    @param content string of the content that will be written
    @optional filename string representing the name of the outputted file
    """
    if filename=='':#if for some reason you want to append everything in one file
        filename = str(time.time_ns())
    f = open(folderpath+"/"+filename+".json", "a")
    f.write(content)
    f.close()

def fetch_line(file, primary_key_field, key_value):
    """
    @require correct csv file "file" with existing "primary_key_field" field.
    @returns the first line found in the csv file where the field 'primary_key_field'
    equals to "key_value". None if no value were found or if file was not found or if the primary_key_field does not exists
    @param file string describing the path to the file
    @param primary_key_field string
    @param key_value string
    """
    if not(os.path.isfile(file)):
        #print("Error : file "+file+"Not found \n")
        return None
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        if primary_key_field in reader.fieldnames:
            for row in reader:
                if row[primary_key_field] == key_value:
                    return row
    return None;

def get_field_value(csv_table, id, fieldname):
    """
    read a csv table with name cvs_table located in config.csv_folder with an id field and a fieldname field,
    and returns the value in fieldname in the first corresponding csvline with the corresponding id field.
    If the csv_table is noexistent, or if fieldname isn't a proper field, or if no corresponding id is found 
    (Or in general, if the function fail), this function returns None.

    @param csv_table the name of the file (without its extension) located in config.csv_folder
    @returns string or None
    """
    csvline = fetch_line(config.csv_folder+"/"+csv_table+".csv","id",id)
    if csvline != None:
        if fieldname in csvline:
            return csvline[fieldname]
    return None

#various_test
if __name__== '__main__':
    import config
    #(old) test of fetch_line on a file
    user_id_100 = fetch_line(config.user_file, "id", "100")
    print(user_id_100['username']+" "+user_id_100['email'])