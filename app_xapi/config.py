"""
configuration file.
TODO : rename these variables with their canonical table name
"""

csv_folder = "data/" #folder in which are stored csv file (not used)
output_folder = "../log_out/" #where json files are produced
user_file = "data/user_20000.csv" #path to csv file with mdl_user csv dump
log_file = "data/log_10000.csv" #path mdl_logstore_standard_log csv dump
moodle_url = "http://moodle-example.com/"#should be the url to the moodle. Used for various IRIs
mdl_course_modules="data/mdl_course_modules.csv"#path to the csv dump of the mdl_course_modules table
mdl_course_modules_completion="data/mdl_course_modules_completion.csv"#path to the csv dump of the mdl_course_modules_completion table
mdl_modules="data/mdl_modules.csv"#path to the csv dump of the mdl_modules table