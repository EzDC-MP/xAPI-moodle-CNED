# Moodle event log into xAPI
## Presentation :
The purpose of this programm is to produce [xAPI 1.0.3 statements](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-About.md#partone) (in form of json file)
of events logged in a Moodle 3.4 database, following [this xAPI profile](https://profiles.adlnet.gov/organization/76fcc051-ef64-4ba4-bfb4-b8035a7d1bf7/profile/e04ed3e2-8927-49c1-a296-2b210d6f269a/version/59c38ed7-428d-44bd-a6c8-bda383a56a92)  

## Notes 
This work is incomplete, see [the implementation instruction file](IMPLEMENTATION.md) to see how the whole program should work, and eventually the [TODO file](TODO.md)

## Getting started

This program solely works from csv file, reflecting the moodle database.

### __Requierments__ :
- Python version should be at least python 3.9.1  
- The [TinCanPython Library](http://rusticisoftware.github.io/TinCanPython/)
- A csv dump of the Moodle SQL database (*see right below*) extracted in the `data` folder.

As for now, the python script does not need a full csv dump of the Moodle database table. To know which table should be extracted for this python script to work, see the tables present under the `#Moodle csv path` comment in the [`config.py` file.](app_xapi/config.py). (Note : as this python script evolves, new tables could be required).

### __Running the script__
When every requirements is met place, the user should then proprely setup variables present in the [`config.py file.`](app_xapi/config.py)
Then simply run the [`main.py`](app_xapi/main.py) script inside the app_xapi folder. json files should be created where the user specified in the [`config.py file`]

### __Notes__
This python script was made during an internship for a specific database. While I believe that the database I used shouldn't differ from other Moodle 3.4 database, data integrity is **not** fully checked before the script runs. 