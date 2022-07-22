"""
configuration file.
"""

#folder in which are stored csv file
csv_folder = "data/" 

#should be the url to the moodle. Used for various IRIs
moodle_url = "http://moodle-example.com/"

#folder where json files are produced
output_folder = "../log_out/"

#Moodle csv table paths
mdl_user = "data/user_20000.csv"    #path to the mdl_user csv dump
mdl_logstore_standard_log = "data/log_10000.csv"    #path to the mdl_logstore_standard_log csv dump
mdl_course_modules="data/mdl_course_modules.csv"    #path to the csv dump of the mdl_course_modules table
mdl_course_modules_completion="data/mdl_course_modules_completion.csv"  #path to the mdl_course_modules_completion csv dump
mdl_modules="data/mdl_modules.csv"  #path to the mdl_modules csv dump