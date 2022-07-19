# Moodle event log into xAPI
## Presentation :
The purpose of this programm is to produce [xAPI 1.0.3 statements](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-About.md#partone) (in form of json file)
of events logged in a Moodle `!!version!!` database, following [this xAPI profile](https://profiles.adlnet.gov/organization/76fcc051-ef64-4ba4-bfb4-b8035a7d1bf7/profile/e04ed3e2-8927-49c1-a296-2b210d6f269a/version/59c38ed7-428d-44bd-a6c8-bda383a56a92)  
This python script requires the [TinCanPython Library](http://rusticisoftware.github.io/TinCanPython/) to be installed.

## How to use
As for now, the python script need a full csv dump of all the tables into the `data` folder from the SQL database produced by the Moodle application. 
The user may also need to proprely set up variable present in the [`config.py`](app_xapi/config.py) file.
When everything is proprely setup, simply run the [`main.py`](app_xapi/main.py) script.

## Notes 
This work is incomplete, see [the implementation instruction file](IMPLEMENTATION.md) to see how the whole program should work