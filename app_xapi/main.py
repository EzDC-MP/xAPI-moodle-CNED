"""
Python script dedicated to take moodle-generated log csv (ver 3.5)
and create .json files describing xAPI statement following rules dictated at 
https://profiles.adlnet.gov/organization/76fcc051-ef64-4ba4-bfb4-b8035a7d1bf7/profile/e04ed3e2-8927-49c1-a296-2b210d6f269a/version/59c38ed7-428d-44bd-a6c8-bda383a56a92
"""

import xapi_resources
import common
import statements
import config
import utils
import uuid
from tincan import (
    Statement,
    Agent,
    Verb,
    Activity,
    Context,
    LanguageMap,
    ActivityDefinition,
    StateDocument,
)

def log_to_statement(csvline):
    """
    Make a statement solely produced off the config.log_file. this function will only process 
    events with edulevel value of 2 and events present in the xapi_resouces.event_list.
    @param csvline a dictionary representing a line of the config.log_file csv file.
    @see csv.DictReader()
    @returns tincan statement if the event was successfully processed. None otherwise
    """
    if csvline['edulevel'] != '2':#Do not process non-educative relevant event.
        return None
    
    eventname = csvline['eventname']
    #print(eventname)
    if eventname in xapi_resources.event_list:
        event_type = xapi_resources.event_list[eventname]
    else:
        return None #event is not supported.

    if event_type=="viewed":
        statement = statements.make_viewed(csvline)
    
    if event_type=="module_completed":

        statement = statements.make_module_completed(csvline)

    return statement

if __name__ == '__main__':
    #Simple tests in main   
    #actor = common.create_agent("102")
    #print(actor.name+".."+actor.mbox)
    #print(actor)

    import csv
    with open(config.log_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            statement = log_to_statement(row)
            if statement != None:
                statement_str=log_to_statement(row).to_json()
                print("writing statement : "+statement_str+"\n\n")
                utils.newjson("log_out", statement_str)